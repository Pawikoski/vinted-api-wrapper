from .base import VintedResponse
from .items import Item
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SearchTrackingParams:
    search_correlation_id: str
    search_session_id: str


@dataclass
class SearchResponse(VintedResponse):
    dominant_brand: Optional[str]
    items: List[Item]
    search_tracking_params: SearchTrackingParams
