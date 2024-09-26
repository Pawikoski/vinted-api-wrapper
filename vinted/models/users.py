from .base import VintedResponse
from .money import MethodPay
from .photos import PhotoHighResolution, PhotoThumbnail
from dataclasses import dataclass
from typing import Optional, Any, List


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
class ShortUser:
    id: int
    login: str
    profile_url: str
    photo: UserPhoto


@dataclass
class Comment:
    comment: Optional[str]
    user: ShortUser


@dataclass
class UserFeedback:
    id: int
    created_at_ts: str
    item_title: str
    item_id: int
    feedback: str
    rating: int
    feedback_rate: int
    feedback_user_id: int
    system_feedback: bool
    is_system_comment: Any
    external_type: Any
    comment: Comment
    user_id: int
    user: ShortUser
    can_change: bool
    can_delete: bool
    created_at: str
    can_comment: bool
    can_change_comment: bool
    can_delete_comment: bool
    localization: Any
    feedback_url: str


@dataclass
class FeedbacksSummary:
    feedback_count: int
    feedback_rating: Optional[str]
    system_feedback_count: int
    system_feedback_rating: Optional[str]
    user_feedback_count: int
    user_feedback_rating: Optional[str]


@dataclass
class UserFeedbacksSummaryResponse(VintedResponse):
    user_feedback_summary: FeedbacksSummary


@dataclass
class UserFeedbacksResponse(VintedResponse):
    user_feedbacks: List[UserFeedback]


@dataclass
class UserResponse(VintedResponse):
    user: DetailedUser
