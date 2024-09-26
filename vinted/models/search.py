from .base import VintedResponse
from .items import Item
from .users import DetailedUser
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


@dataclass
class UserSearchResponse(VintedResponse):
    users: List[DetailedUser]
