from .items import Item
from .other import Pagination
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SearchTrackingParams:
    search_correlation_id: str
    search_session_id: str


@dataclass
class SearchResponse:
    code: int
    dominant_brand: Optional[str]
    items: List[Item]
    pagination: Pagination
    search_tracking_params: SearchTrackingParams
