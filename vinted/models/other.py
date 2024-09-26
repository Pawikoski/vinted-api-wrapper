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
