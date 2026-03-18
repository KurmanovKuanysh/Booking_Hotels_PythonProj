from sqlalchemy.orm import Session
from typing import Any, Optional
from datetime import date

from backend.app.models.room import Room
from backend.app.models.user import User
from backend.app.models.hotel import Hotel
from backend.app.models.booking import Booking
from backend.app.services.booking import BookingService
from backend.app.services.hotel import HotelService
from backend.app.services.room import RoomService
from backend.app.services.user import UserService


class Admin:
    def __init__(self, session: Session):
        self.session = session
        self.user = UserService(session)
        self.hotel = HotelService(session)
        self.booking = BookingService(session)
        self.room = RoomService(session)

        """
        User -> GetALL, Delete, Edit, Add
        Hotel -> GetALL, Delete, Edit, Add
        Booking -> GetALL, Delete, Edit, Add
        Room -> GetALL, Delete, Edit, Add    
        """

    def admin_add_user(self, name: str, email: str, password: str, role: str) -> User | None:
        return  self.user.add_user(name, email, password, role)

    def get_users(self) -> list[User]:
        return self.user.get_users()

    def delete_user(self, user_id: int) -> bool:
        user = self.user.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found!")
        if self.booking.has_confirmed_booking(user_id):
            raise ValueError("User has confirmed bookings!")
        return self.user.delete_user(user_id)

    def edit_user(self, edit: dict[str, Any]):
        return self.user.edit_user(edit)

    def add_new_hotel(self, hotel_name: str, hotel_city: str, hotel_stars: float, hotel_address: str) -> Hotel | None:
        return self.hotel.add_hotel(hotel_name, hotel_city, hotel_stars, hotel_address)

    def edit_hotel(self, edit: dict[str, Any]):
        return self.hotel.edit_hotel(edit)

    def delete_hotel(self, hotel_id: int) -> bool:
        return self.hotel.delete_hotel(hotel_id)

    def get_hotels(self) -> list[Hotel]:
        return self.hotel.get_hotels()

    def add_new_room(
            self,
            hotel_id: int,
            room_number: str,
            room_type_id: int,
            capacity: int,
            price_per_day: float,
            floor: int,
            description: Optional[str] = None
    ) -> Room | None:
        return self.room.add_room(
            h_id=hotel_id,
            room_number=room_number,
            r_t_id=room_type_id,
            capacity=capacity,
            price_per_day=price_per_day,
            floor=floor,
            description=description
        )
    def get_rooms(self) -> list[Room]:
        return self.room.get_rooms()

    def delete_room(self, room_id: int) -> bool:
        return self.room.delete_room(room_id)

    def edit_room(self, edit: dict[str, Any]):
        return self.room.edit_room(edit)

    def add_new_booking(
            self,
            r_id: int,
            check_in: date,
            check_out: date,
            status: str,
            user_id: int
    ) -> Booking | None:
        return self.booking.create_new_booking(
            r_id=r_id,
            check_in=check_in,
            check_out=check_out,
            status=status,
            user_id=user_id
        )

    def get_bookings(self) -> list[Booking]:
        return self.booking.get_all_bookings()

    def delete_booking(self, booking_id: int) -> bool:
        return self.booking.delete_booking(booking_id)

    def edit_booking(self, edit: dict[str, Any]):
        return self.booking.edit_booking(edit)

