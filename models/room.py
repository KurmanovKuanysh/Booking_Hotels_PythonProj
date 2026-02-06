from dataclasses import dataclass

@dataclass
class Room:
    r_id: int
    capacity: int
    floor: int
    type: str
    price_for_day: float
    quantity: int