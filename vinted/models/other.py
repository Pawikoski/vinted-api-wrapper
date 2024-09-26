from dataclasses import dataclass
from typing import Literal


Domain = Literal[
    "pl",
    "fr",
    "at",
    "be",
    "cz",
    "de",
    "dk",
    "es",
    "fi",
    "gr",
    "hr",
    "hu",
    "it",
    "lt",
    "lu",
    "nl",
    "pt",
    "ro",
    "se",
    "sk",
    "co.uk",
    "com",
]

SortOption = Literal[
    "relevance", "price_high_to_low", "price_low_to_high", "newest_first"
]


@dataclass
class Pagination:
    current_page: int
    per_page: int
    time: int
    total_entries: int
    total_pages: int
