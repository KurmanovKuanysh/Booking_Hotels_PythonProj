#check if room exists
from models.hotel import Hotel
from storage import Storage

class HotelService:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.hotels: dict[int, Hotel] = storage.load_hotels()

    def find_by_name(self, name: str) -> dict[int,Hotel]:
        if not name:
            return {}
        hotels_found = {}
        for hotel in self.hotels.values():
            if name.lower() in hotel.name.lower():
                hotels_found[hotel.hotel_id] = hotel
        return hotels_found

    def get_by_id(self, hotel_id: int) -> Hotel | None:
        return self.hotels.get(hotel_id)

    def sort_by_stars(self, min_stars: int, max_stars: int) -> dict[int, Hotel]:
        if min_stars > max_stars:
            return {}
        if min_stars < 1:
            min_stars = 1
        if max_stars > 5:
            max_stars = 5

        hotels_sorted_stars = {}

        for hotel in self.hotels.values():
            if min_stars <= hotel.stars <= max_stars:
                hotels_sorted_stars[hotel.hotel_id] = hotel
        return hotels_sorted_stars