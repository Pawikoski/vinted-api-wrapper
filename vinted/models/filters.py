from .base import VintedResponse
from .photos import PhotoThumbnail
from dataclasses import dataclass
from typing import Any, List, Literal, Optional


@dataclass
class SelectedFilter:
    code: str
    ids: list


@dataclass
class FilterOption:
    id: int
    title: str
    type: Literal["navigational", "group", "default"]
    options: Optional[List["FilterOption"]]


@dataclass
class SearchTranslationsNoResults:
    body: str
    title: str


@dataclass
class SearchTranslations:
    placeholder: Optional[str]
    no_results: Optional[SearchTranslationsNoResults]


@dataclass
class Filter:
    id: int
    title: str
    code: str
    display_type: Literal["hybrid_price", "list", "list_search"]
    selection_type: Literal["default", "multi"]
    is_selection_highlighted: Optional[bool]
    is_new_filter: Optional[bool]
    search_translations: Optional[SearchTranslations]
    options: List[FilterOption]
    position: int


@dataclass
class InitializersFilters:
    query: str
    catalogIds: list
    priceFrom: Any
    priceTo: Any
    currency: Any
    colorIds: list
    brandIds: list
    sizeIds: list
    materialIds: list
    videoGameRatingIds: list
    statusIds: list
    sortBy: Any
    isPopularCatalog: bool
    isPersonalizationDisabled: bool
    catalogFrom: Any
    disableSearchSaving: Any


@dataclass
class CatalogPhoto:
    url: Optional[str]
    thumbnails: Optional[List[PhotoThumbnail]]


@dataclass
class Catalog:
    id: int
    title: str
    code: str
    size_group_id: Optional[int]
    size_group_ids: List[int]
    multiple_size_group_ids: Any
    leaf_multiple_size_group_ids: Any
    shippable: bool
    author_field_visibility: int
    brand_field_visibility: int
    book_title_field_visibility: int
    color_field_visibility: int
    isbn_field_visibility: int
    size_field_visibility: int
    video_game_rating_field_visibility: int
    measurements_field_visibility: bool
    condition_field_visible: bool
    restricted_to_status_id: Any
    landing: Any
    allow_browsing_subcategories: bool
    badge: Any
    package_size_ids: list
    order: int
    item_count: int
    photo: Optional[CatalogPhoto]
    unisex_catalog_id: Any
    catalogs: Optional[List["Catalog"]]
    url: str
    url_en: str


@dataclass
class SelectedDynamicFilter:
    code: str
    ids: list


@dataclass
class InitializersDtos:
    catalogs: List[Catalog]
    dynamicFilters: List[Filter]
    selectedDynamicFilters: List[SelectedDynamicFilter]
    supportedDisplayTypes: list
    selectedDefaultFilters: list


@dataclass
class FiltersResponse(VintedResponse):
    filters: List[Filter]
    selected_filters: List[SelectedFilter]


@dataclass
class InitializersResponse(VintedResponse):
    dtos: InitializersDtos
    filters: InitializersFilters
