import requests
import time

from .endpoints import CATALOG_ITEMS
from .models.search import SearchResponse
from .utils import parse_url_to_params
from dacite import from_dict
from typing import Literal, List


class Vinted:
    def __init__(self, domain: Literal["pl", "fr"] = "pl") -> None:
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
        order: Literal[
            "relevance", "price_high_to_low", "price_low_to_high", "newest_first"
        ] = "newest_first",
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
            url=self.api_url + CATALOG_ITEMS,
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
