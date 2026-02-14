import json
from pathlib import Path

from models.booking import Booking
from models.hotel import Hotel
from models.room import Room
from datetime import datetime

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
HOTELS_PATH = DATA_DIR / "hotels.json"
BOOKINGS_PATH = DATA_DIR / "bookings.json"
ROOMS_PATH = DATA_DIR / "rooms.json"

class Storage:
    @staticmethod
    def load_hotels() -> dict[int,Hotel]:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not HOTELS_PATH.exists():
            return {}
        with open(HOTELS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        hotels: dict[int, Hotel] = {}
        for hotel_data in data:
            hotels[hotel_data["hotel_id"]] = Hotel(
                hotel_id=hotel_data["hotel_id"],
                city=hotel_data["city"],
                name=hotel_data["name"],
                address=hotel_data["address"],
                stars=float(hotel_data["stars"])
            )

        return hotels
    @staticmethod
    def save_hotels(hotels: dict[int, Hotel]) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        hotels_all = []
        for hotel in hotels.values():
            hotel_data = {
                "hotel_id": hotel.hotel_id,
                "city": hotel.city,
                "name": hotel.name,
                "address": hotel.address,
                "stars": hotel.stars
            }
            hotels_all.append(hotel_data)
        with HOTELS_PATH.open("w", encoding="utf-8") as f:
            json.dump(hotels_all, f, ensure_ascii=False, indent=4)
    @staticmethod
    def load_bookings() -> dict[int, Booking]:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not BOOKINGS_PATH.exists():
            return {}
        with BOOKINGS_PATH.open("r",encoding="utf-8") as f:
            data = json.load(f)
        bookings: dict[int, Booking] = {}
        for b in data:
            bookings[b["booking_id"]] = Booking(
                booking_id=b["booking_id"],
                hotel_id=b["hotel_id"],
                r_id=b["r_id"],
                guest_name=b["guest_name"],
                guest_email=b["guest_email"],
                checkin_date=datetime.strptime(b["checkin_date"], "%Y-%m-%d").date(),
                checkout_date=datetime.strptime(b["checkout_date"], "%Y-%m-%d").date(),
                total_price=float(b["total_price"]),
                status=b["status"],
                created_at=datetime.fromisoformat(b["created_at"])
            )
        return bookings
    @staticmethod
    def save_bookings(bookings) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        bookings_all = []
        for booking in bookings.values():
            booking_data = {
                "booking_id": booking.booking_id,
                "hotel_id": booking.hotel_id,
                "r_id": booking.room_id,
                "guest_name": booking.guest_name,
                "guest_email": booking.guest_email,
                "checkin_date": booking.checkin_date.isoformat(),
                "checkout_date": booking.checkout_date.isoformat(),
                "status": booking.status,
                "created_at": booking.created_at.isoformat() + ""
            }
            bookings_all.append(booking_data)
        with BOOKINGS_PATH.open("w", encoding="utf-8") as f:
            json.dump(bookings_all, f, ensure_ascii=False, indent=4)

    @staticmethod
    def load_rooms() -> dict[int, Room]:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not HOTELS_PATH.exists():
            return {}
        with ROOMS_PATH.open("r",encoding="utf-8") as f:
            data = json.load(f)
        rooms: dict[int, Room] = {}
        for r in data:
            rooms[r["r_id"]] = Room(
                r_id = r["r_id"],
                hotel_id=r["hotel_id"],
                number=r["number"],
                type=r["type"],
                capacity=r["capacity"],
                price_for_day=float(r["price_for_day"]),
                floor=r["floor"]
            )
        return rooms

    @staticmethod
    def save_rooms(rooms) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        rooms_all = []
        for r in rooms.values():
            r_data = {
                "r_id": r.r_id,
                "hotel_id": r.hotel_id,
                "number": r.number,
                "type": r.type,
                "capacity": r.capacity,
                "price_for_day": r.price_for_day,
                "floor": r.floor
            }
        rooms_all.append(r_data)
        with ROOMS_PATH.open("w", encoding="utf-8") as f:
            json.dump(rooms_all, f, ensure_ascii=False, indent=4)




