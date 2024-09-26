import requests
import time

from . import endpoints
from .models.search import SearchResponse
from .models.items import ItemsResponse, UserItemsResponse
from .models.other import Domain, SortOption
from .models.users import UserResponse
from .utils import parse_url_to_params
from dacite import from_dict
from typing import List


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
