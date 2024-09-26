from .base import VintedResponse
from .money import CurrencyAmount, Conversion, MethodPay, Price
from .photos import PhotoHighResolution, PhotoThumbnail
from .users import UserPhoto, DetailedUser
from dataclasses import dataclass
from typing import List, Any, Optional
from numbers import Number


@dataclass
class User:
    id: int
    login: str
    profile_url: str
    photo: Optional[UserPhoto]
    business: bool


@dataclass
class BrandDto:
    id: int
    title: Optional[str]
    slug: Optional[str]
    favourite_count: int
    pretty_favourite_count: Optional[str]
    item_count: int
    pretty_item_count: Optional[str]
    is_visible_in_listings: bool
    requires_authenticity_check: bool
    is_luxury: bool
    is_hvf: bool
    path: Optional[str]
    url: Optional[str]
    is_favourite: bool


@dataclass
class ItemBox:
    first_line: Optional[str]
    second_line: Optional[str]


@dataclass
class SearchParams:
    score: Optional[Number]
    matched_queries: Any


@dataclass
class ItemPhoto:
    id: int
    image_no: int
    width: int
    height: int
    dominant_color: Optional[str]
    dominant_color_opaque: Optional[str]
    url: Optional[str]
    is_main: bool
    thumbnails: List[PhotoThumbnail]
    high_resolution: PhotoHighResolution
    is_suspicious: bool
    full_size_url: Optional[str]
    is_hidden: bool
    extra: Any


@dataclass
class Item:
    id: int
    title: str
    price: Optional[Price | str]
    is_visible: bool
    discount: Any
    brand_title: Optional[str]
    user: User
    url: str
    promoted: bool
    photo: ItemPhoto
    favourite_count: int
    is_favourite: bool
    badge: Any
    conversion: Optional[Conversion]
    service_fee: Optional[CurrencyAmount | str]
    total_item_price: Optional[CurrencyAmount | str]
    view_count: int
    size_title: Optional[str]
    content_source: Optional[str]
    status: str
    icon_badges: List[any]
    item_box: Optional[ItemBox]
    search_tracking_params: Optional[SearchParams]


@dataclass
class ItemAttribute:
    code: Optional[str]
    ids: List[int]


@dataclass
class DescriptionAttribute:
    code: Optional[str]
    title: Optional[str]
    value: Optional[str]
    faq_id: Any


@dataclass
class DetailedItem:
    id: int
    title: str
    brand_id: Optional[int]
    size_id: Any
    status_id: int
    user_id: int
    country_id: int
    catalog_id: int
    color1_id: Any
    color2_id: Any
    package_size_id: int
    is_unisex: int
    moderation_status: int
    is_hidden: bool
    is_visible: bool
    is_closed: bool
    favourite_count: int
    active_bid_count: int
    description: str
    package_size_standard: bool
    item_closing_action: Any
    related_catalog_ids: List[Any]
    related_catalogs_enabled: bool
    size: Optional[str]
    brand: Optional[str]
    composition: Optional[str]
    extra_conditions: Optional[str]
    disposal_conditions: Optional[int]
    is_for_sell: bool
    is_handicraft: bool
    is_processing: bool
    is_draft: bool
    is_reserved: bool
    label: Optional[str]
    original_price_numeric: float | str
    currency: Optional[str]
    price_numeric: float | str
    last_push_up_at: Optional[str]
    created_at_ts: Optional[str]
    updated_at_ts: Optional[str]
    user_updated_at_ts: Optional[str]
    is_delayed_publication: bool
    photos: List[ItemPhoto]
    can_be_sold: bool
    can_feedback: bool
    item_reservation_id: Any
    promoted_until: Any
    promoted_internationally: Any
    discount_price_numeric: Any
    author: Any
    book_title: Any
    isbn: Any
    measurement_width: Any
    measurement_length: Any
    measurement_unit: Any
    manufacturer: Any
    manufacturer_labelling: Any
    transaction_permitted: bool
    video_game_rating_id: Any
    item_attributes: List[ItemAttribute]
    user: DetailedUser
    price: CurrencyAmount
    discount_price: Any
    service_fee: Optional[str | float]
    total_item_price: Optional[str | float]
    can_edit: bool
    can_delete: bool
    can_reserve: bool
    can_mark_as_sold: bool
    can_transfer: bool
    instant_buy: bool
    can_close: bool
    can_buy: bool
    can_bundle: bool
    can_ask_seller: bool
    can_favourite: bool
    user_login: Optional[str]
    city_id: Optional[int]
    city: Optional[str]
    country: Optional[str]
    promoted: bool
    is_mobile: bool
    bump_badge_visible: bool
    brand_dto: BrandDto
    catalog_branch_title: str
    path: str
    url: str
    accepted_pay_in_methods: List[MethodPay]
    created_at: str
    color1: Any
    color2: Any
    size_title: Optional[str]
    description_attributes: List[DescriptionAttribute]
    video_game_rating: Any
    status: str
    is_favourite: bool
    view_count: int
    performance: Any
    stats_visible: bool
    can_push_up: bool
    badge: Any
    size_guide_faq_entry_id: Any
    localization: Any
    offline_verification: bool
    offline_verification_fee: Any
    icon_badges: Optional[list]
    item_box: ItemBox


@dataclass
class ItemsResponse(VintedResponse):
    item: DetailedItem


@dataclass
class UserItemsResponse(VintedResponse):
    drafts: Optional[List[DetailedItem]]
    items: List[DetailedItem]
