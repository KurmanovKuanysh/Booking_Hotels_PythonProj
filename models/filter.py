from dataclasses import dataclass
from models.room_types import RoomType
from datetime import date
from typing import Optional

@dataclass
class Filter:
    city: Optional[str] = None
    stars_from: float = 1
    stars_to: float = 5
    capacity: Optional[int] = None
    room_type: Optional[RoomType] = "GENERAL"
    date_from: Optional[date] = None
    date_to: Optional[date] = None
