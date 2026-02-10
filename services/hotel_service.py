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
