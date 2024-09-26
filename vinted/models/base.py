from dataclasses import dataclass
from typing import Optional


@dataclass
class Pagination:
    current_page: int
    per_page: int
    time: int
    total_entries: int
    total_pages: int


@dataclass
class VintedResponse:
    code: int
    pagination: Optional[Pagination]
