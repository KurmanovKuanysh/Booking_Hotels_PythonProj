from typing import Optional

from backend.app.utils.utils import numeric_10_2


class FHotel:
    def __init__(
            self,
            stars_from: numeric_10_2 = 1,
            stars_to: numeric_10_2 = 5,
            city: Optional[str] = None
    ):
        self.stars_from = stars_from
        self.stars_to = stars_to
        self.city:  Optional[str] = city

class FRoom:
    def __init__(
            self,
            capacity: Optional[int] = None,
            min_price: Optional[numeric_10_2] = None,
            max_price: Optional[numeric_10_2] = None,
            room_type: Optional[str] = None
    ):
        self.capacity: Optional[int] = capacity
        self.min_price: Optional[numeric_10_2] = min_price
        self.max_price: Optional[numeric_10_2] = max_price
        self.room_type: Optional[str] = room_type

class FReview:
    def __init__(
            self,
            hotel_id: Optional[int] = None,
            rating: Optional[numeric_10_2] = None
    ):
        self.hotel_id: Optional[int] = hotel_id
        self.rating: Optional[numeric_10_2] = rating