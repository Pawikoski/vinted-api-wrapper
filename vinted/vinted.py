import requests
import time

from . import endpoints
from .models.filters import FiltersResponse, InitializersResponse
from .models.items import ItemsResponse, UserItemsResponse
from .models.other import Domain, SortOption
from .models.search import SearchResponse, UserSearchResponse, SearchSuggestionsResponse
from .models.users import (
    UserResponse,
    UserFeedbacksResponse,
    UserFeedbacksSummaryResponse,
)
from .utils import parse_url_to_params
from dacite import from_dict
from typing import List, Literal


class Vinted:
    def __init__(
        self,
        domain: Domain = "pl",
    ) -> None:
        self.base_url = f"https://www.vinted.{domain}"
        self.api_url = f"{self.base_url}/api/v2"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        }
        self.cookies = self.fetch_cookies()

    def fetch_cookies(self):
        response = requests.get(self.base_url, headers=self.headers)
        return response.cookies

    def search(
        self,
        url: str = None,
        page: int = 1,
        per_page: int = 96,
        search_text: str = None,
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
    ) -> SearchResponse:
        params = {
            "page": page,
            "per_page": per_page,
            "time": time.time(),
            "search_text": search_text,
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
        }
        if url:
            params.update(parse_url_to_params(url))

        response = requests.get(
            url=self.api_url + endpoints.CATALOG_ITEMS,
            headers=self.headers,
            cookies=self.cookies,
            params={
                "page": page,
                "per_page": per_page,
                "time": time.time(),
                "search_text": search_text,
                "catalog_ids": catalog_ids,
                "order": order,
                "size_ids": size_ids,
                "brand_ids": brand_ids,
                "status_ids": status_ids,
                "color_ids": color_ids,
                "patterns_ids": patterns_ids,
                "material_ids": material_ids,
            },
        )
        return from_dict(SearchResponse, response.json())

    def search_users(self, query: str, page: int = 1, per_page: int = 36):
        response = requests.get(
            url=f"{self.api_url}{endpoints.USERS}",
            headers=self.headers,
            cookies=self.cookies,
            params={"page": page, "per_page": per_page, "search_text": query},
        )
        data = response.json()
        return from_dict(UserSearchResponse, data)

    def item_info(self, item_id: int):
        response = requests.get(
            url=f"{self.api_url}{endpoints.ITEMS}/{item_id}",
            headers=self.headers,
            cookies=self.cookies,
        )
        data = response.json()
        return from_dict(ItemsResponse, data)

    def user_info(self, user_id: int, localize: bool = False):
        response = requests.get(
            url=f"{self.api_url}{endpoints.USERS}/{user_id}",
            headers=self.headers,
            cookies=self.cookies,
            params={"localize": localize},
        )
        data = response.json()
        return from_dict(UserResponse, data)

    def user_items(
        self,
        user_id: int,
        page: int = 1,
        per_page: int = 96,
        order: SortOption = "newest_first",
    ):
        response = requests.get(
            url=f"{self.api_url}{endpoints.USERS}/{user_id}/{endpoints.ITEMS}",
            headers=self.headers,
            cookies=self.cookies,
            params={"page": page, "per_page": per_page, "order": order},
        )
        data = response.json()
        return from_dict(UserItemsResponse, data)

    def user_feedbacks(
        self,
        user_id: int,
        page: int = 1,
        per_page: int = 20,
        by: Literal["all", "user", "system"] = "all",
    ):
        response = requests.get(
            url=f"{self.api_url}{endpoints.USER_FEEDBACKS}",
            headers=self.headers,
            cookies=self.cookies,
            params={"user_id": user_id, "page": page, "per_page": per_page, "by": by},
        )
        data = response.json()
        return from_dict(UserFeedbacksResponse, data)

    def user_feedbacks_summary(
        self,
        user_id: int,
    ):
        response = requests.get(
            url=f"{self.api_url}{endpoints.USER_FEEDBACKS_SUMMARY}",
            headers=self.headers,
            cookies=self.cookies,
            params={"user_id": user_id},
        )
        data = response.json()
        return from_dict(UserFeedbacksSummaryResponse, data)

    def search_suggestions(self, query: str):
        response = requests.get(
            url=f"{self.api_url}{endpoints.SEARCH_SUGGESTIONS}",
            headers=self.headers,
            cookies=self.cookies,
            params={"query": query},
        )
        data = response.json()
        return from_dict(SearchSuggestionsResponse, data)

    def catalog_filters(
        self,
        query: str = None,
        catalog_ids: int = None,
        brand_ids: int | List[int] = None,
        status_ids: int | List[int] = None,
        color_ids: int | List[int] = None,
    ):
        response = requests.get(
            url=f"{self.api_url}{endpoints.CATALOG_FILTERS}",
            headers=self.headers,
            cookies=self.cookies,
            params={
                "search_text": query,
                "catalog_ids": catalog_ids,
                "time": time.time(),
                "brand_ids": brand_ids,
                "status_ids": status_ids,
                "color_ids": color_ids,
            },
        )
        data = response.json()
        return from_dict(FiltersResponse, data)

    def catalogs_list(self):
        response = requests.get(
            url=f"{self.api_url}{endpoints.CATALOG_INITIALIZERS}",
            headers=self.headers,
            cookies=self.cookies,
            params={"page": 1, "time": time.time()},
        )
        data = from_dict(InitializersResponse, response.json())
        return data.dtos.catalogs
