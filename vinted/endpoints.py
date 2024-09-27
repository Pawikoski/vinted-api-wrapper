from enum import Enum


class Endpoints(Enum):
    CATALOG_ITEMS = "/catalog/items"
    CATALOG_FILTERS = "/catalog/filters"
    CATALOG_INITIALIZERS = "/catalog/initializers"
    ITEMS = "/items/{}"
    USERS = "/users"
    USER = "/users/{}"
    USER_FEEDBACKS = "/user_feedbacks"
    USER_ITEMS = "/users/{}/items"
    USER_FEEDBACKS_SUMMARY = "/user_feedbacks/summary"
    SEARCH_SUGGESTIONS = "/search_suggestions"
