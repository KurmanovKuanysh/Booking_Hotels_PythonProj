from sqlalchemy import select, update
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
        if self.get_hotel_by_name(name):
            raise HTTPException(status_code=409, detail="Hotel with this name already exists")
        if self.get_hotel_by_address(address):
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
            if not hotel:
                raise HTTPException(status_code=404, detail="Hotel not found")
            if self.hotel_have_active_booking(hotel_id):
                raise HTTPException(status_code=409, detail="Hotel have active booking")
            rooms = self.session.scalars(select(Room).where(Room.h_id == hotel_id)).all()
            for room in rooms:
                self.session.delete(room)
            self.session.delete(hotel)
            self.session.commit()
            return True
        except HTTPException as e:
            self.session.rollback()
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

    def get_hotel_by_address(self,address: str) -> Hotel | None:
        hotel = self.session.scalar(
            select(Hotel)
            .where(Hotel.address == address.strip())
        )
        return hotel

    def get_hotel_by_name(self, name:str) -> list[Hotel] | None:
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

    def edit_hotel(self, edit: dict) -> Hotel:
        if "id" not in edit:
            raise ValueError("Hotel id is required")
        hotel = self.get_hotel_by_id(edit["id"])
        if hotel is None:
            raise ValueError("Hotel not found")

        if "name" in edit and edit["name"] is not None:
            if len(edit["name"]) < 3:
                raise ValueError("Hotel name must be at least 3 characters long")
            if len(edit["name"]) > 100:
                raise ValueError("Hotel name must be at most 100 characters long")
            if self.session.scalars(select(Hotel).where(Hotel.name == edit["name"], Hotel.id != hotel.id)).all():
                raise ValueError("Hotel name already exists on Hotels")
            hotel.name = edit["name"].strip()

        if "city" in edit and edit["city"] is not None:
            if len(edit["city"]) < 3:
                raise ValueError("Hotel city must be at least 3 characters long")
            if len(edit["city"]) > 100:
                raise ValueError("Hotel city must be at most 100 characters long")
            hotel.city = edit["city"].strip()

        if "address" in edit and edit["address"] is not None:
            if len(edit["address"]) < 3:
                raise ValueError("Address must be at least 3 characters long")
            if self.session.scalars(select(Hotel).where(Hotel.address == edit["address"], Hotel.id != hotel.id)).all():
                raise ValueError("Address already exists on Hotels")
            hotel.address = edit["address"]

        if "stars" in edit and edit["stars"] is not None:
            if not isinstance(edit["stars"], float):
                raise ValueError("Stars must be a float")
            if not edit["stars"] > 0.0 and not edit["stars"] <= 5.0:
                raise ValueError("Stars must be between 1 and 5")
            hotel.stars = edit["stars"]
        self.session.commit()
        self.session.refresh(hotel)

        return hotel
