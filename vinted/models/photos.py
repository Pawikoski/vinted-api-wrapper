from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class PhotoHighResolution:
    id: str
    timestamp: int
    orientation: Any


@dataclass
class PhotoThumbnail:
    type: str
    url: Optional[str]
    width: Optional[int]
    height: Optional[int]
    original_size: Optional[bool]
