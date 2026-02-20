from models.booking import Booking
from models.room import Room
from services.rooms_service import RoomsService
from storage import Storage
from datetime import datetime, date

def parse_date(date_in: str, date_out:str):
    return datetime.strptime(date_in, "%Y-%m-%d").date(), datetime.strptime(date_out, "%Y-%m-%d").date()

def check_date_range(checkin_date, checkout_date):
    return checkin_date <= checkout_date

class BookingService:
    def __init__(self, storage: Storage, rooms_service: RoomsService):
        self.storage = storage
        self.bookings: dict[int, Booking] = storage.load_bookings()
        self.room_service = rooms_service

    def create_new_booking_reserve(self,hotel_id:int,r_id:int,name_client:str,checkin_date,checkout_date,email_client: str) -> bool:
        #checkin/out now is "date type"
        room = self.room_service.get_by_id(r_id)
        new_id = max(self.bookings.keys()) + 1
        days = (checkout_date - checkin_date).days + 1
        price = room.price_for_day*days

        new_booking = Booking(
            booking_id=new_id,
            hotel_id=hotel_id,
            r_id=r_id,
            guest_name=name_client,
            guest_email=email_client,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            total_price=price,
            status = "pending",
            created_at=datetime.now()
        )
        self.bookings[new_id] = new_booking
        return True


    def check_availability(self,rooms:dict[int, Room],hotel_id:int,room_id:int,checkin_date:date,checkout_date:date) -> tuple[bool,str]:
        if room_id not in rooms:
            return False, "Room not found"
        if hotel_id != rooms[room_id].hotel_id:
            return False, "Room belongs to another hotel, recheck ur filters"
        if not check_date_range(checkin_date,checkout_date):
            return False, "Checkout date have to be after checkin date"
        for booking in self.bookings.values():
            if booking.room_id == room_id:
                if not checkout_date <= booking.checkin_date or checkin_date >= booking.checkout_date:
                    return False, "Room is not free, for that date range"
        return True, "Room is available!"

    def get_user_bookings(self, user_email: str) -> dict[int, Booking] | None:
        user_bookings = {}
        for booking in self.bookings.values():
            if booking.guest_email != user_email:
                continue
            if booking.status != "confirmed":
                continue
            user_bookings[booking.booking_id] = booking
        return user_bookings

    def get_all_bookings(self) -> dict[int, Booking] | None:
        return self.bookings

    def get_booking_by_id(self, booking_id: int) -> Booking | None:
        return self.bookings.get(booking_id)

    def get_hotel_id_by_booking_id(self, booking_id: int) -> int | None:
        return self.bookings.get(booking_id).hotel_id


    def get_room_id_by_booking_id(self, booking_id: int) -> int | None:
        return self.bookings.get(booking_id).r_id