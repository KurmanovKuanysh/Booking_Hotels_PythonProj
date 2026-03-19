from sqlalchemy import select, update, func
from sqlalchemy.orm import Session
from backend.app.models.hotel import Hotel
from backend.app.models.booking import Booking
from backend.app.models.room import Room
from datetime import date

from fastapi import HTTPException

class HotelService:
    def __init__(self, session: Session):
        self.session = session
    def add_hotel(
            self,
            name: str,
            city: str,
            stars: float,
            address: str,
            description: str = None
    ):
        existing_name = self.session.scalar(select(Hotel).where(func.lower(Hotel.name) == name.strip().lower()))
        if existing_name:
            raise HTTPException(status_code=409, detail="Hotel with this name already exists")
        existing_address = self.session.scalar(select(Hotel).where(func.lower(Hotel.address) == address.strip().lower()))
        if existing_address:
            raise HTTPException(status_code=409, detail="Hotel with this address already exists")

        hotel = Hotel(
            name=name,
            city=city,
            address=address,
            stars=stars,
            description=description
        )
        self.session.add(hotel)
        self.session.commit()
        self.session.refresh(hotel)
        return hotel

    def delete_hotel(self, hotel_id: int) -> bool:
        try:
            hotel = self.get_hotel_by_id(hotel_id)
            if self.hotel_have_active_booking(hotel_id):
                raise HTTPException(status_code=409, detail="Hotel have active booking")
            rooms = self.session.scalars(select(Room).where(Room.h_id == hotel_id)).all()
            for room in rooms:
                self.session.delete(room)
            self.session.delete(hotel)
            self.session.commit()
            return True
        except HTTPException:
            raise
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Error deleting hotel: {e}")

    def get_hotels(self) -> list[Hotel]:
        return list(self.session.scalars(select(Hotel)).all())

    def get_hotel_by_id(self, hotel_id: int) -> Hotel | None:
        hotel = self.session.scalars(select(Hotel).where(Hotel.id == hotel_id)).first()
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")
        return hotel

    def list_hotels_by_city(self, city: str) -> list[Hotel]:
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

    def list_hotels_by_stars(self, stars_from: float, stars_to: float) -> list[Hotel]:
        if stars_from < 1 or stars_from > 5:
            raise HTTPException(status_code=400, detail="Stars must be between 1 and 5")
        if stars_from > stars_to:
            stars_from, stars_to = stars_to, stars_from
        hotels = self.session.scalars(
            select(Hotel).where(Hotel.stars >= stars_from, Hotel.stars <= stars_to)
        ).all()
        return list(hotels)

    def list_hotels_by_filter(
            self,
            stars_from: float | float = 1,
            stars_to: float | float = 5,
            city: str | None = None,
    ) -> list[Hotel]:
        hotels = select(Hotel).where(Hotel.stars >= stars_from, Hotel.stars <= stars_to)
        if city is not None:
            hotels = hotels.where(Hotel.city.ilike(f"%{city}%"))

        return list(self.session.scalars(hotels).all())

    def hotel_have_active_booking(self, hotel_id: int) -> bool:
        hotel_active = (
            select(Hotel)
            .join(Room, Room.h_id == Hotel.id)
            .join(Booking, Booking.r_id == Room.id)
            .where(
                Hotel.id == hotel_id,
                Booking.status.in_(["confirmed", "pending"]),
                Booking.check_out >= date.today())
        )
        return bool(self.session.scalars(hotel_active).first())

    def list_hotels_with_active_booking(self) -> list[Hotel]:
        hotels_active = (
            select(Hotel)
            .join(Room, Room.h_id == Hotel.id)
            .join(Booking, Booking.r_id == Room.id)
            .where(
                Booking.status.in_(["confirmed", "pending"]),
                Booking.check_out >= date.today()
            ).distinct()
        )
        return list(self.session.scalars(hotels_active).all())

    from fastapi import HTTPException
    from sqlalchemy import select

    def edit_hotel(
            self,
            hotel_id: int,
            name: str | None = None,
            city: str | None = None,
            address: str | None = None,
            stars: float | None = None,
            description: str | None = None
    ) -> Hotel:
        hotel = self.get_hotel_by_id(hotel_id)
        if hotel is None:
            raise HTTPException(status_code=404, detail="Hotel not found")

        if name is not None:
            name = name.strip()
            if len(name) < 3:
                raise HTTPException(status_code=400, detail="Hotel name must be at least 3 characters long")
            if len(name) > 100:
                raise HTTPException(status_code=400, detail="Hotel name must be at most 100 characters long")
            same_name = self.session.scalar(
                select(Hotel).where(
                    func.lower(Hotel.name) == name.lower(),
                    Hotel.id != hotel.id
                )
            )
            if same_name:
                raise HTTPException(status_code=409, detail="Hotel name already exists")
            hotel.name = name

        if city is not None:
            city = city.strip()

            if len(city) < 3:
                raise HTTPException(status_code=400, detail="Hotel city must be at least 3 characters long")
            if len(city) > 100:
                raise HTTPException(status_code=400, detail="Hotel city must be at most 100 characters long")

            hotel.city = city

        if address is not None:
            address = address.strip()

            if len(address) < 3:
                raise HTTPException(status_code=400, detail="Address must be at least 3 characters long")

            same_address = self.session.scalar(
                select(Hotel).where(
                    func.lower(Hotel.address) == address.lower(),
                    Hotel.id != hotel.id
                )
            )
            if same_address:
                raise HTTPException(status_code=409, detail="Address already exists on Hotels")
            hotel.address = address
        if stars is not None:
            if stars < 1.0 or stars > 5.0:
                raise HTTPException(status_code=400, detail="Stars must be between 1 and 5")
            hotel.stars = stars
        if description is not None:
            description = description.strip()

            if len(description) > 255:
                raise HTTPException(status_code=400, detail="Description must be at most 255 characters long")
            hotel.description = description
        self.session.commit()
        self.session.refresh(hotel)

        return hotel
