from models.room import Room
from storage import Storage
from models.room_types import RoomType
from models.booking import Booking
from datetime import date
from models.booking_status import BookingStatus

class RoomsService:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.rooms: dict[int, Room] = storage.load_rooms()
        self.room_types = RoomType

    def get_by_hotel_id(self, h_id:int) -> dict[int,Room]:
        rooms_in_hotel = {}
        for room in self.rooms.values():
            if room.hotel_id == h_id:
                rooms_in_hotel[room.r_id] = room
        return rooms_in_hotel

    def get_by_id(self, r_id:int) -> Room | None:
        return self.rooms.get(r_id)

    def get_by_price_range(self, min_price: int, max_price: int) -> dict[int, Room]:
        rooms_found = {}
        for room in self.rooms.values():
            if min_price <= room.price_for_day <= max_price:
                rooms_found[room.r_id] = room
        return rooms_found

    def get_price_range(self, rooms_new:dict[int,Room]) -> dict:
        min_price = 0
        max_price = max(rooms_new.values(), key=lambda x: x.price_for_day).price_for_day
        ranges = {
            "min_price": min_price,
            "max_price": max_price
        }
        return ranges

    def sort_by_price(self, min_price: int, max_price: int) -> dict[int, Room]:
        if min_price > max_price:
            return {}
        if min_price < 0:
            min_price = 0
        if max_price > 1000000:
            max_price = 1000000
        rooms_found = {}
        for room in self.rooms.values():
            if min_price <= room.price_for_day <= max_price:
                rooms_found[room.r_id] = room
        return rooms_found

    def sort_by_type(self, room_type: str) -> dict[int, Room]:
        if room_type not in self.room_types:
            return {}
        rooms_found = {}
        room_type = room_type.upper()
        for room in self.rooms.values():
            if room.type == room_type:
                rooms_found[room.r_id] = room
        return rooms_found

    def sort_by_capacity(self, persona: int) -> dict[int, Room]:
        if persona < 1:
            return {}
        rooms_found = {}
        for room in self.rooms.values():
            if room.capacity >= persona:
                rooms_found[room.r_id] = room
        return rooms_found

    def get_available_rooms(self, bookings: dict[int,Booking]) -> dict[int, Room]:
        a_rooms: dict[int, Room] = {}
        book = {b.r_id for b in bookings.values()}
        for room in self.rooms.values():
            if room.r_id not in book:
                a_rooms[room.r_id] = room
        return a_rooms

    # NOT (new_checkout <= existing_checkin OR new_checkin >= existing_checkout)
    @staticmethod
    def is_available_rooms(room_id:int, booking: dict[int,Booking], check_in:date, check_out:date) -> bool:
        for b in booking.values():
            if b.r_id != room_id:
                continue
            if b.status not in (BookingStatus.PENDING, BookingStatus.CONFIRMED):
                continue
            x = not (check_out <= b.checkin_date or check_in >= b.checkout_date)
            if x:
                return False
        return True













