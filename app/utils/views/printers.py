from app.models.booking import Booking
from app.models.user import User
from app.models.hotel import Hotel
from app.models.room import Room
from app.models.room_type import RoomType

class Printer:
    def __init__(self,hotel, room, booking, user):
        self.hotel = hotel
        self.room = room
        self.booking = booking
        self.user = user

    def print_user_bookings(self, user_bookings: list[Booking]):
        if not user_bookings:
            print("No bookings found")
            return
        print("User Bookings:")
        for b in user_bookings:
            room = self.room.get_room_by_id(b.r_id)
            hotel = self.hotel.get_hotel_by_id(room.h_id)
            user = self.user.get_user_by_id(b.user_id)

            print("=" * 50)

            print(f"{'Booking ID:':<15}{b.id}")
            print(f"{'Guest Name:':<15}{user.name}")
            print(f"{'Email:':<15}{user.email}")

            print("-" * 55)

            print(f"{'Hotel:':<15}{hotel.name if hotel else 'N/A'}")
            print(f"{'City:':<15}{hotel.city if hotel else 'N/A'}")
            print(f"{'Room ID:':<15}{room.id if room else 'N/A'}")
            print(f"{'Capacity:':<15}{room.capacity if room else 'N/A'}")
            print(f"{'Price/day:':<15}{room.price_per_day if room else 'N/A'}")

            print("-" * 55)

            print(f"{'Check-in:':<15}{b.check_in}")
            print(f"{'Check-out:':<15}{b.check_out}")

            print("-" * 55)

            print(f"{'Total price:':<15}{room.price_per_day * (b.check_out - b.check_in).days}")

            print("-" * 55)

    def print_room_types(self, room_types: list[RoomType]):
        for room_type in room_types:
            print(f"{room_type.id} - {room_type.type_name}")

    def print_room(self, room: Room):
        print(f"{'ID':<4}{'CAP':<6}{'TYPE':<12}{'HOTEL':<8}{'FLOOR':<7}{'PRICE/DAY':<10}")
        print(f"{room.id:<4}{room.capacity:<6}{room.r_t_id:<12}{room.h_id:<8}{room.floor:<7}{room.price_per_day:<10}")

    def print_rooms(self, rooms: list[Room]):
        print("Rooms for Hotel:")
        print(f"{'ID':<4}{'CAP':<6}{'TYPE':<12}{'HOTEL':<8}{'FLOOR':<7}{'PRICE/DAY':<10}")
        for room in rooms:
            print(f"{room.id:<4}{room.capacity:<6}{room.r_t_id:<12}{room.h_id:<8}{room.floor:<7}{room.price_per_day:<10}")

    def print_hotel(self, hotel: Hotel):
        print(f"{'ID': <3}{'NAME': <19}{'CITY': <20}{'STARS': <10}")
        print(f"{hotel.id: <3}{hotel.name: <19}{hotel.city: <20}{hotel.stars: <10}")

    def print_hotels(self, hotels: list[Hotel]):
        print(f"{'ID': <3}{'NAME': <19}{'CITY': <20}{'STARS': <10}")
        for hotel in hotels:
            print(f"{hotel.id:<3}{hotel.name:<19}{hotel.city:<20}{hotel.stars:<10}")

