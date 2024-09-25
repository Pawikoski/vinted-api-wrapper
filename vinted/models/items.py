from dataclasses import dataclass
from typing import List, Any, Optional
from numbers import Number


@dataclass
class Price:
    amount: Optional[str]
    currency_code: Optional[str]


@dataclass
class PhotoThumbnail:
    type: str
    url: Optional[str]
    width: Optional[int]
    height: Optional[int]
    original_size: Optional[bool]


@dataclass
class PhotoHighResolution:
    id: str
    timestamp: int
    orientation: Any


@dataclass
class UserPhoto:
    id: int
    width: Optional[int]
    height: Optional[int]
    temp_uuid: Any
    url: Optional[str]
    dominant_color: Optional[str]
    dominant_color_opaque: Optional[str]
    thumbnails: List[PhotoThumbnail]
    is_suspicious: bool
    orientation: Any
    high_resolution: Optional[PhotoHighResolution]
    full_size_url: Optional[str]
    is_hidden: bool
    extra: Any


@dataclass
class User:
    id: int
    login: str
    profile_url: str
    photo: Optional[UserPhoto]
    business: bool


@dataclass
class Discount:
    minimal_item_count: int
    fraction: Optional[str]


@dataclass
class BundleDiscount:
    id: int
    user_id: int
    enabled: bool
    minimal_item_count: int
    fraction: Optional[str]
    discounts: List[Discount]


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
class UserVerificationOption:
    valid: bool
    verified_at: Optional[Any]
    available: bool


@dataclass
class UserVerification:
    email: UserVerificationOption
    facebook: UserVerificationOption
    google: UserVerificationOption


@dataclass
class MethodPay:
    id: int
    code: Optional[str]
    requires_credit_card: Optional[bool]
    event_tracking_code: Optional[str]
    icon: Optional[str]
    enabled: Optional[bool]
    translated_name: Optional[str]
    note: Optional[str]
    method_change_possible: bool


@dataclass
class DetailedUser:
    id: int
    anon_id: str
    login: str
    real_name: Any
    email: Any
    birthday: Any
    item_count: int
    given_item_count: int
    taken_item_count: int
    followers_count: int
    following_count: int
    following_brands_count: int
    positive_feedback_count: int
    neutral_feedback_count: int
    negative_feedback_count: int
    meeting_transaction_count: Optional[int]
    account_status: int
    feedback_reputation: float
    feedback_count: int
    is_on_holiday: bool
    is_publish_photos_agreed: bool
    expose_location: bool
    third_party_tracking: bool
    default_address: Any
    last_loged_on_ts: str
    city_id: Optional[int]
    city: str
    country_id: int
    country_code: str
    country_iso_code: str
    country_title: str
    contacts_permission: Any
    contacts: Any
    photo: Optional[UserPhoto]
    path: str
    moderator: bool
    is_catalog_moderator: bool
    is_catalog_role_marketing_photos: bool
    hide_feedback: bool
    allow_direct_messaging: bool
    bundle_discount: Optional[BundleDiscount]
    fundraiser: Any
    business_account_id: Any
    has_ship_fast_badge: bool
    total_items_count: int
    about: str
    verification: UserVerification
    avg_response_time: Any
    carrier_ids: Optional[List[int]]
    carriers_without_custom_ids: Optional[List[int]]
    locale: str
    updated_on: int
    is_hated: bool
    hates_you: bool
    is_favourite: bool
    profile_url: str
    share_profile_url: str
    facebook_user_id: Any
    is_online: bool
    can_view_profile: bool
    can_bundle: bool
    country_title_local: str
    last_loged_on: Optional[str]
    accepted_pay_in_methods: List[MethodPay]
    localization: Any
    is_bpf_price_prominence_applied: bool
    msg_template_count: int
    is_account_banned: bool
    account_ban_date: Any
    is_account_ban_permanent: bool
    business_account: Any
    business: bool


@dataclass
class CurrencyAmount:
    amount: Optional[str]
    currency_code: Optional[str]


@dataclass
class Conversion:
    seller_price: Optional[str]
    seller_currency: Optional[str]
    buyer_currency: Optional[str]
    fx_rounded_rate: Optional[str]
    fx_base_amount: Optional[str]
    fx_markup_rate: Optional[str]


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
