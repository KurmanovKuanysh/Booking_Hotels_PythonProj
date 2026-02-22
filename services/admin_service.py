from models.hotel import Hotel
from models.room import Room
from models.room_types import RoomType
from storage import Storage


class Admin():
    def __init__(self, storage: Storage):
        self.storage = storage

    def add_new_hotel(
            self,
            hotels:dict[int,Hotel],
            hotel_id:int,
            name:str,
            city:str,
            stars:float,
            address:str
    ) -> tuple[bool, str]:

        if hotel_id in hotels:
            return False, "Hotel already exists!"
        if not name or not city or stars <= 0:
            return False, "Invalid hotel details"
        new_hotel = Hotel(
            hotel_id = int(hotel_id),
            city = city.strip().capitalize(),
            name = name.strip().capitalize(),
            address= address.strip().capitalize(),
            stars = float(stars)
        )
        hotels[hotel_id] = new_hotel
        if self.storage.save_hotels(hotels):
            return True, "Hotel added successfully"
        return False, "Failed to add hotel"


    def edit_exist_hotel(self, hotels: dict[int, Hotel], hotel_id: int | None, new_name: str | None, new_city: str | None, new_star: float | None) -> tuple[bool, str]:
        if hotel_id is None or hotel_id not in hotels:
            return False, "Hotel not found!"
        indicator = False
        if new_name is not None:
            hotels[hotel_id].name = new_name.strip().capitalize()
            indicator = True
        if new_city is not None:
            hotels[hotel_id].city = new_city.strip().capitalize()
            indicator = True
        if new_star is not None:
            hotels[hotel_id].stars = float(new_star)
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

    def add_new_room(
            self,
            rooms: dict[int, Room],
            hotels: dict[int, Hotel],
            hotel_id: int,
            number: str,
            room_type: str,
            capacity: int,
            price_for_day: float,
            floor: int
    ) -> tuple[bool, str]:
        if hotel_id not in hotels:
            return False, "Hotel not found!"
        if not number.strip():
            return False, "Room number can't be empty!"
        if capacity < 1:
            return False, "Invalid room capacity!(need to be greater than 0)"
        if price_for_day <= 0:
            return False, "Invalid room price per day!"
        if floor < 0:
            return False, "Invalid room floor!"
        number = number.strip()
        room_type = getattr(RoomType, room_type.strip().upper(), RoomType.GENERAL)

        for r in rooms.values():
            if r.hotel_id == hotel_id and r.number == number:
                return False, f"Room with number {number} already exists in hotel {hotels[hotel_id].name}!"
        new_r_id = max(rooms.keys(), default=0) + 1

        new_room = Room(
            r_id = int(new_r_id),
            hotel_id = int(hotel_id),
            number = number,
            type = room_type,
            capacity = int(capacity),
            price_for_day = float(price_for_day),
            floor = int(floor)
        )
        rooms[new_r_id] = new_room
        if self.storage.save_rooms(rooms):
            return True, "Room added successfully!"
        return False, "Failed to add room!"

    def edit_room(
            self,
            rooms: dict[int, Room],
            room_id: int,
            new_number: str | None,
            new_type: str | None,
            new_capacity: int | None,
            new_price: float | None,
            new_floor: int | None
    ) -> tuple[bool, str]:
        if room_id not in rooms:
            return False, "Room not found!"
        indicator = False
        if new_number is not None:
            for r in rooms.values():
                if r.hotel_id == rooms[room_id].hotel_id and r.number == new_number.strip():
                    if r.r_id == room_id:
                        continue
                    return False, f"Room with number {new_number} already exists in hotel {rooms[room_id].hotel_id}!"
            rooms[room_id].number = new_number.strip()
            indicator = True
        if new_type is not None:
            rooms[room_id].type = getattr(RoomType, new_type.strip().upper(), RoomType.GENERAL)
            indicator = True
        if new_capacity is not None:
            if new_capacity < 1:
                return False, "Invalid room capacity!(need to be greater than 0)"
            rooms[room_id].capacity = int(new_capacity)
            indicator = True
        if new_price is not None:
            if new_price <= 0:
                return False, "Invalid room price per day!"
            rooms[room_id].price_for_day = float(new_price)
            indicator = True
        if new_floor is not None:
            if new_floor < 0:
                return False, "Invalid room floor!"
            rooms[room_id].floor = int(new_floor)
            indicator = True
        if indicator:
            self.storage.save_rooms(rooms)
            return True, "Room details updated successfully!"
        return False, "No details to update!"
