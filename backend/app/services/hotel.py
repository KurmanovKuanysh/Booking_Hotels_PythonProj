from sqlalchemy import select, func
from sqlalchemy.orm import Session

from backend.app.core.exceptions import HotelAlreadyExistsError, HotelNotFoundError, HotelHaveBookingsError, \
    InvalidNumberError
from backend.app.schemas.hotel import HotelCreate
from backend.app.models.filter import FHotel
from backend.app.models.hotel import Hotel
from backend.app.models.booking import Booking, Status
from backend.app.models.room import Room
from datetime import date

class HotelService:
    def __init__(self, session: Session):
        self.session = session
    def add_hotel(
            self,
            data: HotelCreate
    ):
        existing_name = self.session.scalar(select(Hotel).where(func.lower(Hotel.name) == data.name.strip().lower()))
        if existing_name:
            raise HotelAlreadyExistsError
        existing_address = self.session.scalar(select(Hotel).where(func.lower(Hotel.address) == data.address.strip().lower()))
        if existing_address:
            raise HotelAlreadyExistsError

        hotel = Hotel(
            name=data.name,
            city=data.city,
            address=data.address,
            stars=data.stars,
            description=data.description
        )
        self.session.add(hotel)
        self.session.commit()
        self.session.refresh(hotel)
        return hotel

    def delete_hotel(self, hotel_id: int) -> bool:
        hotel = self.get_hotel_by_id(hotel_id)
        if self.hotel_have_active_booking(hotel_id):
            raise HotelHaveBookingsError

        self.session.delete(hotel)
        self.session.commit()
        return True

    def get_hotels(self, limit: int, offset: int) -> list[Hotel] | None:
        return list(self.session.scalars(
            select(Hotel)
            .limit(limit)
            .offset(offset)
        ).all())

    def get_hotel_by_id(self, hotel_id: int) -> Hotel | None:
        hotel = self.session.scalar(select(Hotel).where(Hotel.id == hotel_id))
        if not hotel:
            raise HotelNotFoundError
        return hotel

    def get_popular_hotels(self, limit: int) -> list[Hotel]:
        popular_hotels = list(self.session.scalars(
            select(Hotel)
            .join(Room, Room.h_id == Hotel.id)
            .join(Booking, Booking.r_id == Room.id)
            .where(Booking.status.in_([Status.CONFIRMED, Status.COMPLETED]))
            .group_by(Hotel.id)
            .order_by(func.count(Booking.id).desc())
            .limit(limit)
        ))
        return popular_hotels

    def list_hotels_by_city(self, city: str) -> list[Hotel] | None:
        hotels = self.session.scalars(
            select(Hotel).where(Hotel.city == city.strip().lower())
        ).all()
        return list(hotels)

    def get_hotels_by_address(self,address: str) -> list[Hotel] | list[None]:
        hotel = list(self.session.scalars(
            select(Hotel)
            .where(Hotel.address.ilike(f"%{address.strip()}%"))
        ).all())
        return hotel

    def get_hotels_by_name(self, name:str) -> list[Hotel] | None:
        hotel = self.session.scalars(
            select(Hotel).where(Hotel.name.ilike(f"%{name.strip().lower()}%"))
        ).all()
        return list(hotel)

    def list_hotels_by_stars(self, stars_from: int, stars_to: int) -> list[Hotel]:
        if stars_from < 1 or stars_from > 5:
            raise InvalidNumberError
        if stars_from > stars_to:
            stars_from, stars_to = stars_to, stars_from
        hotels = self.session.scalars(
            select(Hotel).where(Hotel.stars >= stars_from, Hotel.stars <= stars_to)
        ).all()
        return list(hotels)

    def list_hotels_by_filter(
            self,
            filters = FHotel()
    ) -> list[Hotel]:
        hotels = select(Hotel).where(Hotel.stars >= filters.stars_from, Hotel.stars <= filters.stars_to)
        if filters.city is not None:
            hotels = hotels.where(Hotel.city.ilike(f"%{filters.city}%"))

        return list(self.session.scalars(hotels).all())

    def hotel_have_active_booking(self, hotel_id: int) -> bool:
        hotel_active = (
            select(Hotel)
            .join(Room, Room.h_id == Hotel.id)
            .join(Booking, Booking.r_id == Room.id)
            .where(
                Hotel.id == hotel_id,
                Booking.status.in_([Status.CONFIRMED, Status.PENDING]),
                Booking.check_out >= date.today())
        )
        return bool(self.session.scalar(hotel_active))


    def edit_hotel(
            self,
            hotel_id: int,
            data
    ) -> Hotel:
        hotel = self.get_hotel_by_id(hotel_id)
        if data.name is not None:
            name = data.name.strip()
            same_name = self.session.scalar(
                select(Hotel).where(
                    func.lower(Hotel.name) == name.lower(),
                    Hotel.id != hotel.id
                )
            )
            if same_name:
                raise HotelAlreadyExistsError
            hotel.name = name

        if data.city is not None:
            city = data.city.strip().title()
            hotel.city = city

        if data.address is not None:
            address = data.address.strip().title()

            same_address = self.session.scalar(
                select(Hotel).where(
                    func.lower(Hotel.address).ilike(f"%{address.lower()}%"),
                    Hotel.id != hotel.id
                )
            )
            if same_address:
                raise HotelAlreadyExistsError
            hotel.address = address

        if data.stars is not None:
            hotel.stars = data.stars

        if data.description is not None:
            hotel.description = data.description.strip()

        self.session.commit()
        self.session.refresh(hotel)

        return hotel
