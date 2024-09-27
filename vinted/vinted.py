import requests
import time

from .endpoints import Endpoints
from .models.base import VintedResponse
from .models.filters import FiltersResponse, InitializersResponse, Catalog
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

    def _call(self, method: Literal["get"], *args, **kwargs):
        return requests.request(
            method=method, headers=self.headers, cookies=self.cookies, *args, **kwargs
        )

    def _get(
        self,
        endpoint: Endpoints,
        response_model: VintedResponse,
        format_values=None,
        wanted_status_code: int = 200,
        *args,
        **kwargs,
    ):
        if format_values:
            url = self.api_url + endpoint.value.format(format_values)
        else:
            url = self.api_url + endpoint.value
        response = self._call(method="get", url=url, *args, **kwargs)
        if response.status_code != wanted_status_code and not kwargs.get("recursive"):
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
            return from_dict(response_model, json_response)
        except requests.exceptions.JSONDecodeError:
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
    ) -> SearchResponse:
        params = {
            "page": page,
            "per_page": per_page,
            "time": time.time(),
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
        }
        if url:
            params.update(parse_url_to_params(url))

        return self._get(Endpoints.CATALOG_ITEMS, SearchResponse, params=params)

    def search_users(
        self, query: str, page: int = 1, per_page: int = 36
    ) -> UserSearchResponse:
        params = {"page": page, "per_page": per_page, "search_text": query}
        return self._get(Endpoints.USERS, UserSearchResponse, params=params)

    def item_info(self, item_id: int) -> ItemsResponse:
        return self._get(Endpoints.ITEMS, ItemsResponse, item_id)

    def user_info(self, user_id: int, localize: bool = False) -> UserResponse:
        params = {"localize": localize}
        return self._get(Endpoints.USER, UserResponse, user_id, params=params)

    def user_items(
        self,
        user_id: int,
        page: int = 1,
        per_page: int = 96,
        order: SortOption = "newest_first",
    ) -> UserItemsResponse:
        params = {"page": page, "per_page": per_page, "order": order}
        return self._get(
            Endpoints.USER_ITEMS, UserItemsResponse, user_id, params=params
        )

    def user_feedbacks(
        self,
        user_id: int,
        page: int = 1,
        per_page: int = 20,
        by: Literal["all", "user", "system"] = "all",
    ) -> UserFeedbacksResponse:
        params = {"user_id": user_id, "page": page, "per_page": per_page, "by": by}
        return self._get(Endpoints.USER_FEEDBACKS, UserFeedbacksResponse, params=params)

    def user_feedbacks_summary(
        self,
        user_id: int,
    ) -> UserFeedbacksSummaryResponse:
        params = {"user_id": user_id}
        return self._get(
            Endpoints.USER_FEEDBACKS_SUMMARY,
            UserFeedbacksSummaryResponse,
            params=params,
        )

    def search_suggestions(self, query: str) -> SearchSuggestionsResponse:
        return self._get(
            Endpoints.SEARCH_SUGGESTIONS,
            SearchSuggestionsResponse,
            params={"query": query},
        )

    def catalog_filters(
        self,
        query: str = None,
        catalog_ids: int = None,
        brand_ids: int | List[int] = None,
        status_ids: int | List[int] = None,
        color_ids: int | List[int] = None,
    ) -> FiltersResponse:
        params = {
            "search_text": query,
            "catalog_ids": catalog_ids,
            "time": time.time(),
            "brand_ids": brand_ids,
            "status_ids": status_ids,
            "color_ids": color_ids,
        }
        return self._get(Endpoints.CATALOG_FILTERS, FiltersResponse, params=params)

    def catalogs_list(self) -> List[Catalog]:
        data: InitializersResponse = self._get(
            Endpoints.CATALOG_INITIALIZERS,
            InitializersResponse,
            params={"page": 1, "time": time.time()},
        )
        return data.dtos.catalogs
