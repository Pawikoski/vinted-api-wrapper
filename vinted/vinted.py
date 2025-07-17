import logging
import time
import math
import random
from copy import deepcopy
from typing import List, Literal
from urllib.parse import urlencode, urlparse, urlunparse

import cloudscraper
from bs4 import BeautifulSoup
from dacite import from_dict
from fake_useragent import UserAgent

from .endpoints import Endpoints
from .exceptions import RateLimitExceededException
from .models.base import VintedResponse
from .models.filters import Catalog, FiltersResponse, InitializersResponse
from .models.items import ItemsResponse, UserItemsResponse
from .models.other import Domain, Language, SortOption
from .models.search import SearchResponse, SearchSuggestionsResponse, UserSearchResponse, ShippingResponse
from .models.users import (
    UserFeedbacksResponse,
    UserFeedbacksSummaryResponse,
    UserResponse,
)
from .utils import parse_url_to_params

# Set up logging - datetime format, level, and format
# Default to INFO level, but allow users to change it via logging.getLogger(__name__).setLevel()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,  # Set to DEBUG to capture all levels, individual loggers can filter
)

logger = logging.getLogger(__name__)
# Set default level to INFO, but users can override with logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

ua = UserAgent(platforms=['windows', 'macos'], browsers=['chrome', 'firefox', 'safari'])
# Use a consistent user agent throughout the session to avoid detection
# Choose a recent Chrome user agent for better compatibility


class Vinted:
    def __init__(
        self, domain: Domain = "pl", language: Language = "en-US", proxy: str = None
    ) -> None:
        """
        Initialize Vinted client with specified domain, language, and optional proxy.
        Each domain can access its own language plus English and a few others (which depends on the domain) for API responses.

        Args:
            domain: Vinted domain to use (e.g., "pl", "com", "fr")
            language: Language for API responses (e.g., "en-US", "pl-PL")
            proxy: Optional proxy URL for requests
        """
        logger.info(
            f"Initializing Vinted client with domain: {domain}, language: {language}, proxy: {'enabled' if proxy else 'disabled'}"
        )

        self.proxy = None
        if proxy:
            self.proxy = {"http": proxy, "https": proxy}
            logger.debug(f"Proxy configuration set: {self.proxy}")

        self.base_url = f"https://www.vinted.{domain}"
        self.api_url = f"{self.base_url}/api/v2"
        self.host = f"www.vinted.{domain}"
        self.user_agent = ua.random

        logger.debug(f"Base URL: {self.base_url}, API URL: {self.api_url}")        
        
        self.headers = {
            # Basic request headers
            "User-Agent": self.user_agent,
            "Host": self.host,
            
            # Accept headers
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": f"{language},*;q=0.5",
            
            # Connection and transfer headers
            "Connection": "keep-alive",
            "TE": "Trailers",
            
            # Security and privacy headers
            "DNT": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Upgrade-Insecure-Requests": "1",
            
            # Priority header
            "Priority": "u=0, i",
        }

        logger.debug(f"Headers configured: {self.headers}")

        # Initialize cloudscraper session
        self.scraper = cloudscraper.create_scraper()
        logger.debug("Cloudscraper session initialized")

        self.cookies = self.fetch_cookies()
        logger.info("Vinted client initialization completed successfully")

    def set_log_level(self, level: int) -> None:
        """
        Set the logging level for the Vinted module.

        Args:
            level: Logging level (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR)

        Example:
            import logging
            vinted = Vinted()
            vinted.set_log_level(logging.DEBUG)  # Enable debug logging
        """
        logger.setLevel(level)
        logger.info(f"Logging level set to: {logging.getLevelName(level)}")

    def update_proxy(self, proxy: str) -> None:
        """
        Update the proxy configuration for the Vinted client.

        Args:
            proxy: Proxy URL to be used for requests.

        Example:
            vinted.update_proxy("http://username:password@proxyserver:port")
        """
        self.proxy = {"http": proxy, "https": proxy}
        logger.info(f"Proxy updated: {self.proxy}")

    def fetch_cookies(self):
        logger.debug(f"Fetching cookies from: {self.base_url}")

        headers = {
            "User-Agent": self.user_agent,
            "Host": self.host,
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Connection": "keep-alive",
            "TE": "trailers",
            "DNT": "1"
        }

        response = self.scraper.head(
            f"{self.base_url}/how_it_works", headers=headers, proxies=self.proxy, allow_redirects=True
        )
        logger.info(
            f"Cookies fetched successfully, status code: {response.status_code}"
        )
        logger.debug(f"Cookies: {response.cookies}")
        return response.cookies

    def update_cookies(self, cookies=None) -> None:
        """
        Update or refresh cookies for the session.

        Args:
            cookies: Optional cookies to set. If None, fetches new cookies.

        Example:
            vinted.update_cookies()  # Refresh cookies
            vinted.update_cookies(custom_cookies)  # Set custom cookies
        """
        if cookies is None:
            logger.info("Refreshing cookies from server")
            self.cookies = self.fetch_cookies()
        else:
            logger.info("Setting custom cookies")
            self.cookies = cookies
            logger.debug(f"Updated cookies: {self.cookies}")

    def _call(self, method: Literal["get"], *args, **kwargs):
        logger.debug(
            f"Making {method.upper()} request with args: {args}, kwargs: {kwargs}"
        )

        if params := kwargs.pop("params", {}):
            logger.debug(f"Processing parameters: {params}")
            updated_params = deepcopy(params)

            # Replace None values with empty strings
            processed_params = {
                k: "" if v is None else v for k, v in updated_params.items()
            }
            logger.debug(
                f"Processed parameters (None -> empty string): {processed_params}"
            )

            # Encode parameters with '+' left untouched
            encoded_params = urlencode(processed_params, safe="+")
            logger.debug(f"Encoded parameters: {encoded_params}")

            # Assign updated params directly to the url as string
            updated_url = kwargs.get("url")
            updated_url = urlunparse(
                urlparse(updated_url)._replace(query=encoded_params)
            )
            kwargs["url"] = updated_url
            logger.debug(f"Final URL with parameters: {updated_url}")

        if "recursive" in kwargs:
            del kwargs["recursive"]

        # Handle custom headers
        headers = kwargs.pop("headers", self.headers)
        if headers != self.headers:
            logger.debug(f"Using custom headers: {headers}")

        logger.info(
            f"Executing {method.upper()} request to: {kwargs.get('url', 'unknown URL')}"
        )
        response = self.scraper.request(
            method=method,
            headers=headers,
            cookies=self.cookies,
            proxies=self.proxy,
            *args,
            **kwargs,
        )
        logger.info(f"Response size: {len(response.content) / 1024:.2f} KB")
        logger.info(f"Request completed with status code: {response.status_code}")
        if response.status_code == 429:
            logger.error("Rate limit exceeded (HTTP 429)")
            raise RateLimitExceededException(
                "Rate limit exceeded. Please try again later."
            )
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        logger.debug(f"Response content: {response.text[:100]}...")  # Log
        return response

    def _get(
        self,
        endpoint: Endpoints,
        response_model: VintedResponse,
        format_values=None,
        wanted_status_code: int = 200,
        *args,
        **kwargs,
    ):
        logger.debug(
            f"GET request to endpoint: {endpoint.value}, format_values: {format_values}, expected status: {wanted_status_code}"
        )

        if format_values:
            url = self.api_url + endpoint.value.format(format_values)
            logger.debug(f"Formatted endpoint URL: {url}")
        else:
            url = self.api_url + endpoint.value
            logger.debug(f"Standard endpoint URL: {url}")

        response = self._call(method="get", url=url, *args, **kwargs)

        if response.status_code != wanted_status_code and not kwargs.get("recursive"):
            logger.info(
                f"Status code {response.status_code} != expected {wanted_status_code}, refreshing cookies and retrying"
            )
            self.fetch_cookies()
            return self._get(
                endpoint=endpoint,
                response_model=response_model,
                format_values=format_values,
                wanted_status_code=wanted_status_code,
                recursive=True,
                *args,
                **kwargs,
            )

        try:
            json_response = response.json()
            logger.debug(f"Successfully parsed JSON response from {endpoint.value}")
            result = from_dict(response_model, json_response)
            logger.info(f"Successfully converted response to {response_model.__name__}")
            return result
        except Exception as e:
            logger.error(f"Failed to parse JSON response from {endpoint.value}: {e}")
            return {"error": f"HTTP {response.status_code}"}

    def search(
        self,
        url: str = None,
        page: int = 1,
        per_page: int = 96,
        query: str = None,
        price_from: float = None,
        price_to: float = None,
        order: SortOption = "newest_first",
        catalog_ids: int | List[int] = None,
        size_ids: int | List[int] = None,
        brand_ids: int | List[int] = None,
        status_ids: int | List[int] = None,
        color_ids: int | List[int] = None,
        patterns_ids: int | List[int] = None,
        material_ids: int | List[int] = None,
        video_game_platform_ids: int | List[int] = None,
        country_ids: str | List[str] = None,
    ) -> SearchResponse:
        logger.info(
            f"Starting search - query: '{query}', page: {page}, per_page: {per_page}, order: {order}"
        )
        logger.debug(
            f"Search filters - price_from: {price_from}, price_to: {price_to}, catalog_ids: {catalog_ids}"
        )
        logger.debug(
            f"Additional filters - size_ids: {size_ids}, brand_ids: {brand_ids}, status_ids: {status_ids}"
        )
        logger.debug(
            f"More filters - color_ids: {color_ids}, patterns_ids: {patterns_ids}, material_ids: {material_ids}"
        )
        logger.debug(
            f"Platform/country filters - video_game_platform_ids: {video_game_platform_ids}, country_ids: {country_ids}"
        )

        params = {
            "page": page,
            "per_page": per_page,
            "time": math.floor(time.time() - random.random() * 60 * 3),
            "search_text": query,
            "price_from": price_from,
            "price_to": price_to,
            "catalog_ids": catalog_ids,
            "order": order,
            "size_ids": size_ids,
            "brand_ids": brand_ids,
            "status_ids": status_ids,
            "color_ids": color_ids,
            "patterns_ids": patterns_ids,
            "material_ids": material_ids,
            "video_game_platform_ids": video_game_platform_ids,
            "country_ids": country_ids,
        }
        if url:
            logger.debug(f"Parsing additional parameters from URL: {url}")
            params.update(parse_url_to_params(url))

        logger.debug(f"Final search parameters: {params}")
        
        # Add Referer header only if url parameter is provided
        headers = self.headers.copy()
        if url:
            headers["Referer"] = url
            logger.debug(f"Added Referer header: {headers['Referer']}")
        
        result = self._get(Endpoints.CATALOG_ITEMS, SearchResponse, params=params, headers=headers)
        logger.info("Search completed successfully")
        return result

    def search_users(
        self, query: str, page: int = 1, per_page: int = 36
    ) -> UserSearchResponse:
        logger.info(
            f"Searching users with query: '{query}', page: {page}, per_page: {per_page}"
        )
        params = {"page": page, "per_page": per_page, "search_text": query}
        logger.debug(f"User search parameters: {params}")
        result = self._get(Endpoints.USERS, UserSearchResponse, params=params)
        logger.info("User search completed successfully")
        return result

    def item_info(self, item_id: int) -> ItemsResponse:
        logger.info(f"Fetching item info for item_id: {item_id}")
        result = self._get(Endpoints.ITEMS, ItemsResponse, item_id)
        logger.info(f"Item info retrieved successfully for item_id: {item_id}")
        return result

    def user_info(self, user_id: int, localize: bool = False) -> UserResponse:
        logger.info(f"Fetching user info for user_id: {user_id}, localize: {localize}")
        params = {"localize": localize}
        logger.debug(f"User info parameters: {params}")
        result = self._get(
            Endpoints.USER, UserResponse, user_id, params=params
        )  # this raises 'dacite.exceptions.MissingValueError: missing value for field "user"' for non valid user id
        logger.info(f"User info retrieved successfully for user_id: {user_id}")
        return result

    def user_items(
        self,
        user_id: int,
        page: int = 1,
        per_page: int = 96,
        order: SortOption = "newest_first",
    ) -> UserItemsResponse:
        logger.info(
            f"Fetching user items for user_id: {user_id}, page: {page}, per_page: {per_page}, order: {order}"
        )
        params = {"page": page, "per_page": per_page, "order": order}
        logger.debug(f"User items parameters: {params}")
        result = self._get(
            Endpoints.USER_ITEMS, UserItemsResponse, user_id, params=params
        )
        logger.info(f"User items retrieved successfully for user_id: {user_id}")
        return result

    def user_feedbacks(
        self,
        user_id: int,
        page: int = 1,
        per_page: int = 20,
        by: Literal["all", "user", "system"] = "all",
    ) -> UserFeedbacksResponse:
        logger.info(
            f"Fetching user feedbacks for user_id: {user_id}, page: {page}, per_page: {per_page}, by: {by}"
        )
        params = {"user_id": user_id, "page": page, "per_page": per_page, "by": by}
        logger.debug(f"User feedbacks parameters: {params}")
        result = self._get(
            Endpoints.USER_FEEDBACKS, UserFeedbacksResponse, params=params
        )
        logger.info(f"User feedbacks retrieved successfully for user_id: {user_id}")
        return result

    def user_feedbacks_summary(
        self,
        user_id: int,
    ) -> UserFeedbacksSummaryResponse:
        logger.info(f"Fetching user feedbacks summary for user_id: {user_id}")
        params = {"user_id": user_id}
        logger.debug(f"User feedbacks summary parameters: {params}")
        result = self._get(
            Endpoints.USER_FEEDBACKS_SUMMARY,
            UserFeedbacksSummaryResponse,
            params=params,
        )
        logger.info(
            f"User feedbacks summary retrieved successfully for user_id: {user_id}"
        )
        return result

    def search_suggestions(self, query: str) -> SearchSuggestionsResponse:
        logger.info(f"Fetching search suggestions for query: '{query}'")
        result = self._get(
            Endpoints.SEARCH_SUGGESTIONS,
            SearchSuggestionsResponse,
            params={"query": query},
        )
        logger.info("Search suggestions retrieved successfully")
        return result

    def catalog_filters(
        self,
        query: str = None,
        catalog_ids: int = None,
        brand_ids: int | List[int] = None,
        status_ids: int | List[int] = None,
        color_ids: int | List[int] = None,
    ) -> FiltersResponse:
        logger.info(
            f"Fetching catalog filters - query: '{query}', catalog_ids: {catalog_ids}"
        )
        logger.debug(
            f"Filter parameters - brand_ids: {brand_ids}, status_ids: {status_ids}, color_ids: {color_ids}"
        )
        params = {
            "search_text": query,
            "catalog_ids": catalog_ids,
            "time": time.time(),
            "brand_ids": brand_ids,
            "status_ids": status_ids,
            "color_ids": color_ids,
        }
        logger.debug(f"Catalog filters parameters: {params}")
        result = self._get(Endpoints.CATALOG_FILTERS, FiltersResponse, params=params)
        logger.info("Catalog filters retrieved successfully")
        return result

    def catalogs_list(self) -> List[Catalog]:
        logger.info("Fetching catalogs list")
        params = {"page": 1, "time": time.time()}
        logger.debug(f"Catalogs list parameters: {params}")
        data: InitializersResponse = self._get(
            Endpoints.CATALOG_INITIALIZERS,
            InitializersResponse,
            params=params,
        )
        logger.info(
            f"Catalogs list retrieved successfully, found {len(data.dtos.catalogs)} catalogs"
        )
        return data.dtos.catalogs
    
    def fetch_shipping_details(self, item_id: int) -> ShippingResponse:
        """
        Fetches shipping details for a specific item.
        
        Args:
            item_id: The ID of the item to fetch shipping details for
            
        Returns:
            ShippingResponse: Contains shipping details including pickup options, 
                            multiple shipping options availability, free shipping status,
                            pricing information, and potential discounts
                            
        Raises:
            RateLimitExceededException: If rate limit is exceeded
            requests.exceptions.HTTPError: If the request fails
            
        Example:
            shipping = vinted.fetch_shipping_details(123456)
            if shipping.shipping_details.free_shipping:
                print("Free shipping available!")
            print(f"Shipping price: {shipping.shipping_details.price.amount} {shipping.shipping_details.price.currency_code}")
        """
        logger.info(f"Fetching shipping details for item_id: {item_id}")
        logger.debug(f"Requesting shipping details from endpoint: {Endpoints.SHIPPING_DETAILS.value}")
        
        try:
            result = self._get(Endpoints.SHIPPING_DETAILS, ShippingResponse, item_id)
            logger.info(f"Shipping details retrieved successfully for item_id: {item_id}")
            logger.debug(f"Response code: {result.code}, Free shipping: {result.shipping_details.free_shipping}")
            return result
        except Exception as e:
            logger.error(f"Failed to fetch shipping details for item_id {item_id}: {e}")
            raise
        
    def fetch_offer_description(self, url: str) -> str:
        """
        Fetches the offer description from a given Vinted item URL.
        :param url: The URL of the Vinted item.
        :return: The description of the item.
        """
        logger.info(f"Fetching offer description from URL: {url}")
        try:
            logger.debug("Making request to fetch offer description")
            response = self.scraper.get(
                url, headers=self.headers, proxies=self.proxy, cookies=self.cookies
            )
            if response.status_code == 200:
                logger.debug("Parsing HTML response for description")
                soup = BeautifulSoup(response.text, "html.parser")
                description = soup.find("div", {"itemprop": "description"})
                if description:
                    description_text = description.get_text(strip=True)
                    logger.info(
                        f"Description found, length: {len(description_text)} characters"
                    )
                    logger.debug(f"Description content: {description_text[:100]}...")
                    return description_text
                else:
                    logger.error("Description not found in the page.")
                    return None
            else:
                logger.error(f"Error fetching description: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"An error occurred while fetching the description: {e}")
            return None
        

        
