from services.hotel_service import HotelService
from storage import Storage
from services.booking_service import BookingService
from services.rooms_service import RoomsService
from models.filter import Filter

storage = Storage()

rooms_service = RoomsService(storage)
rooms = storage.load_rooms()
hotels_service = HotelService(storage)
bookings = storage.load_bookings()
bookings_service = BookingService(storage, rooms_service)
filters = Filter()

print(rooms_service.get_available_rooms(bookings))



