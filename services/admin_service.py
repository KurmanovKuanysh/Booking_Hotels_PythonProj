from models.hotel import Hotel
from storage import Storage


class Admin():
    def __init__(self, storage: Storage):
        self.storage = storage

    def add_new_hotel(self,hotels:dict[int,Hotel],hotel_id:int,name:str,city:str,stars:int,address:str) -> tuple[bool, str]:
        if hotel_id in hotels:
            return False, "Hotel already exists!"
        if not name or not city or stars <= 0:
            return False, "Invalid hotel details"
        new_hotel = Hotel(
            hotel_id,
            name,
            city,
            address,
            stars)
        hotels[hotel_id] = new_hotel
        self.storage.save_hotels(hotels)
        return True, "Hotel added successfully"

    def edit_hotel(self, hotels: dict[int, Hotel], hotel_id: int | None, new_name: str | None, new_city: str | None, new_star: int | None):
        if hotel_id is None or hotel_id not in hotels:
            return False, "Hotel not found!"
        indicator = False
        if new_name is not None:
            hotels[hotel_id].name = new_name
            indicator = True
        if new_city is not None:
            hotels[hotel_id].city = new_city
            indicator = True
        if new_star is not None:
            hotels[hotel_id].stars = new_star
            indicator = True
        if indicator:
            self.storage.save_hotels(hotels)
            return True, "Hotel details updated successfully!"
        return False, "No details to update!"


    def delete_hotel(self, hotels: dict[int, Hotel], hotel_id: int) -> tuple[bool, str]:
        if hotel_id not in hotels:
            return False, "Hotel not found!"
        del hotels[hotel_id]
        self.storage.save_hotels(hotels)
        return True, "Hotel deleted successfully!"
