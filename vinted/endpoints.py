from enum import Enum


class Endpoints(Enum):
    CATALOG_ITEMS = "/catalog/items"
    CATALOG_FILTERS = "/catalog/filters"
    CATALOG_INITIALIZERS = "/catalog/initializers"
    ITEMS = "/items/{}/details"  # Old endpoint /items/{id} is deprecated, use /items/{id}/details instead
    USERS = "/users"
    USER = "/users/{}"
    USER_FEEDBACKS = "/user_feedbacks"
    USER_ITEMS = "/users/{}/items"
    USER_FEEDBACKS_SUMMARY = "/user_feedbacks/summary"
    SEARCH_SUGGESTIONS = "/search_suggestions"
    SHIPPING_DETAILS = "/items/{}/shipping_details"