from storage import Storage
from services.booking_service import BookingService

storage = Storage()
hotels = storage.load_hotels()
bookings = storage.load_bookings()
rooms = storage.load_rooms()
booking_service = BookingService()

booking_service.create_new_booking(bookings, rooms, 1, 1, "John", "2021-01-01", "2021-01-02")
storage.save_bookings(bookings)

while True:
    menu_main()