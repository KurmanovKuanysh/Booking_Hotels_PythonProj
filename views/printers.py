from models.booking import Booking
from models.filter import Filter
from models.hotel import Hotel
from models.room import Room
from models.room_types import RoomType


def show_active_filters(filters: dict):
    if not filters:
        print("No active filters")
        return
    print("Current Filters:")
    for key, value in filters.items():
        print(f"{key}: {value}")

def print_hotels(hotels: dict[int, Hotel]):
    print("\nHotel List:")
    print(f"{'ID': <3}{'NAME': <19}{'CITY': <15}{'STARS': <10}")
    for hotel in hotels.values():
        print(f"{hotel.hotel_id: <3}{hotel.name: <19}{hotel.city: <15}{hotel.stars: <10}")

def print_rooms(rooms: dict[int, Room], hotel_id: int | None = None):
    print("\nRoom List:")
    print(f"{'ID': <3}{'HOTEL ID': <19}{'CAPACITY': <15}")
    for room in rooms.values():
        print(f"{room.r_id: <3}{room.hotel_id: <19}{room.capacity: <15}")


def print_room_types(room_types: RoomType):
    print("\nRoom Types Available:")
    print(getattr(room_types, "DELUXE", None))
    print(getattr(room_types, "GENERAL", None))
    print(getattr(room_types, "PRESIDENT", None))
    print(getattr(room_types, "FAMILY", None))

def show_user_bookings(bookings: dict[int, Booking], hotels: dict[int, Hotel], rooms: dict[int, Room]):
    if not bookings:
        print("No bookings found!")
        return
    print("\nYOUR BOOKINGS\n")

    for b in bookings.values():
        hotel = hotels.get(b.hotel_id)
        room = rooms.get(b.r_id)

        print("=" * 55)

        # --- Guest info ---
        print(f"{'Booking ID:':<15}{b.booking_id}")
        print(f"{'Guest Name:':<15}{b.guest_name}")
        print(f"{'Email:':<15}{b.guest_email}")

        print("-" * 55)

        # --- Hotel + Room ---
        print(f"{'Hotel:':<15}{hotel.name if hotel else 'N/A'}")
        print(f"{'City:':<15}{hotel.city if hotel else 'N/A'}")
        print(f"{'Room ID:':<15}{room.r_id if room else 'N/A'}")
        print(f"{'Capacity:':<15}{room.capacity if room else 'N/A'}")
        print(f"{'Price/day:':<15}{room.price_for_day if room else 'N/A'}")

        print("-" * 55)

        # --- Dates ---
        print(f"{'Check-in:':<15}{b.checkin_date}")
        print(f"{'Check-out:':<15}{b.checkout_date}")

        print("-" * 55)

        # --- Total ---
        print(f"{'Total price:':<15}{b.total_price}")

        print("=" * 55)