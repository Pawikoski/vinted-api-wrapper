from .base import VintedResponse
from .items import Item
from .users import DetailedUser
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DominantBrand:
    id: int
    title: str
    slug: str
    favourite_count: int
    pretty_favourite_count: str
    item_count: int
    pretty_item_count: str
    is_visible_in_listings: bool
    requires_authenticity_check: bool
    is_luxury: bool
    is_hvf: bool
    path: str
    url: str
    is_favourite: bool


@dataclass
class SearchTrackingParams:
    search_correlation_id: str
    search_session_id: str


@dataclass
class SearchSuggestionParam:
    title: List[str]
    entity_combination: List[str]
    source: List[str]
    search_signals: List[str]


@dataclass
class SearchSuggestion:
    title: str
    total_score: int
    origin_id: int
    params: List[SearchSuggestionParam]
    suggestion_id: int
    suggestion_type: int


@dataclass
class SearchResponse(VintedResponse):
    dominant_brand: Optional[DominantBrand]
    items: List[Item]
    search_tracking_params: SearchTrackingParams


@dataclass
class UserSearchResponse(VintedResponse):
    users: List[DetailedUser]


@dataclass
class SearchSuggestionsResponse(VintedResponse):
    search_suggestions: List[SearchSuggestion]
