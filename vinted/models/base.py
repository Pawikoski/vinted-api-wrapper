from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class Pagination:
    current_page: int
    per_page: int
    time: int
    total_entries: int
    total_pages: int


@dataclass
class VintedResponse:
    code: Literal[
        -200,
        -100,
        -99,
        0,
        10,
        20,
        21,
        99,
        50,
        51,
        52,
        100,
        102,
        103,
        104,
        105,
        106,
        107,
        108,
        110,
        112,
        113,
        114,
        115,
        116,
        117,
        118,
        119,
        121,
        122,
        123,
        124,
        127,
        128,
        129,
        130,
        131,
        134,
        136,
        140,
        142,
        143,
        146,
        152,
        156,
        158,
    ]
    pagination: Optional[Pagination]
