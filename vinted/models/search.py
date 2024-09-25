from .items import Item
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SearchTrackingParams:
    search_correlation_id: str
    search_session_id: str


@dataclass
class Pagination:
    current_page: int
    per_page: int
    time: int
    total_entries: int
    total_pages: int


@dataclass
class SearchResponse:
    code: int
    dominant_brand: Optional[str]
    items: List[Item]
    pagination: Pagination
    search_tracking_params: SearchTrackingParams
