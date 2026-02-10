from models.booking import Booking
from models.room import Room
from storage import Storage



def check_date_range(checkin_date, checkout_date):
    return checkin_date <= checkout_date

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


    def check_availability(self,rooms:dict[int, Room],hotel_id,room_id,checkin_date,checkout_date) -> tuple[bool,str]:
        if hotel_id not in rooms:
            return False, "Hotel not found"
        if room_id not in rooms:
            return False, "Room not found"
        for booking in self.bookings.values():
            if booking.room_id == room_id:
                if not checkout_date <= booking.checkin_date and not checkin_date >= booking.checkout_date:
                    return False, "Room is not available on date"
                return False, "Room is already booked"
        return True, "Room is available"
