from models.booking import Booking
from models.room import Room
from storage import Storage

class BookingService:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.bookings: dict[int, Booking] = storage.load_bookings()

    def create_new_booking(self, rooms:dict[int, Room],hotel_id,room_id,name_client,checkin_date,checkout_date):
        room = rooms[room_id]
        new_id = max(self.bookings.keys()) + 1
        price = room.price_for_day * 5
        new_booking = Booking(
            booking_id=new_id,
            hotel_id=hotel_id,
            room_id=room_id,
            name_client=name_client,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            total_price=price,
            status = "confirmed"
        )
        self.bookings[new_id] = new_booking
        print("New order, BOOKED!")
