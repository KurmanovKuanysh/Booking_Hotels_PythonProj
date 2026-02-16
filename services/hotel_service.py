#check if room exists
from models.booking import Booking
from models.hotel import Hotel
from storage import Storage
from models.room import Room

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

    def find_by_city(self, city: str) -> dict[int,Hotel]:
        if not city:
            return {}
        hotels_found = {}
        for hotel in self.hotels.values():
            if city.lower() in hotel.city.lower():
                hotels_found[hotel.hotel_id] = hotel
        return hotels_found

    def get_by_id(self, hotel_id: int) -> Hotel | None:
        return self.hotels.get(hotel_id)

    def sort_by_stars(self, min_stars: float, max_stars: float) -> dict[int, Hotel]:
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

    def get_price_range(self, rooms: dict[int, Room], min_price: float, max_price: float) -> dict[int, list]:
        hotel_id_price_range = {}
        for hotel in self.hotels.values():
            room_price = []
            for room in rooms.values():
                if room.hotel_id == hotel.hotel_id:
                    room_price.append(room.price_for_day)
            room_price.sort()
            if max_price >= room_price[-1] and min_price <= room_price[0]:
                hotel_id_price_range[hotel.hotel_id] = room_price
                print(hotel_id_price_range[hotel.hotel_id])
        return hotel_id_price_range

    def get_hotels_by_capacity(self, rooms: dict[int, Room], capacity: int) -> dict[int, Hotel]:
        hotels_by_capacity = {}
        for hotel in self.hotels.values():
            for room in rooms.values():
                if room.hotel_id == hotel.hotel_id and room.capacity >= capacity:
                    hotels_by_capacity[hotel.hotel_id] = hotel
        return hotels_by_capacity

