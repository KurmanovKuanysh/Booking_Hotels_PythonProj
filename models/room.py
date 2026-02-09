from dataclasses import dataclass
from models.room_types import RoomType

@dataclass
class Room:
    r_id: int
    hotel_id: int
    number: str
    type: RoomType
    capacity: int
    price_for_day: float
    floor: int