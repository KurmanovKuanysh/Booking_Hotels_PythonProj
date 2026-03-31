from typing import Optional

class FHotel:
    def __init__(
            self,
            stars_from: int = 1,
            stars_to: int = 5,
            city: Optional[str] = None
    ):
        self.stars_from = stars_from
        self.stars_to = stars_to
        self.city:  Optional[str] = city

class FRoom:
    def __init__(
            self,
            capacity: Optional[int] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None,
            room_type: Optional[str] = None
    ):
        self.capacity: Optional[int] = capacity
        self.min_price: Optional[float] = min_price
        self.max_price: Optional[float] = max_price
        self.room_type: Optional[str] = room_type