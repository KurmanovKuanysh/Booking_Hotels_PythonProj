from dataclasses import dataclass

from models.room import Room


@dataclass
class Hotel:
    hotel_id: int
    city: str
    name: str
    rooms: list[ Room]
    floors: int
    address: str
    stars: float

