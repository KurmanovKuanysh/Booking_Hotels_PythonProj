from app.services.hotel_service import *

class HotelServiceSQL:
    def list_all(self):
        return list_hotels()

    def get_by_id(self, hotel_id: int):
        return get_hotel_by_id(hotel_id)

    def find_by_name(self, name: str):
        return find_hotels_by_name(name)

    def add_hotel(self, name: str, city: str, address: str, stars: float) -> int:
        return create_hotel(name, city, address, stars)

    def delete_hotel(self, hotel_id: int):
        return delete_hotel(hotel_id)