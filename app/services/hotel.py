from sqlalchemy import select, update
from sqlalchemy.orm import Session
from app.models.hotel import Hotel
from app.models.booking import Booking
from app.models.room import Room
from datetime import date

class HotelService:
    def __init__(self, session: Session):
        self.session = session
    def add_hotel(self, name: str, city: str, stars: float, address: str):
        hotel = Hotel(
            name=name,
            city=city,
            address=address,
            stars=stars
        )
        self.session.add(hotel)
        self.session.commit()
        self.session.refresh(hotel)
        return hotel

    def delete_hotel(self, hotel_id: int):
        try:
            self.session.execute(
                update(Hotel)
                .where(Hotel.id == hotel_id)
                .values(is_deleted=True)
            )
            self.session.commit()
            self.session.refresh(Hotel)
        except Exception as e:
            print(f"Error deleting hotel: {e}")
            raise

    def get_hotel_by_id(self, hotel_id: int) -> Hotel | None:
        hotel = self.session.scalars(select(Hotel).where(Hotel.id == hotel_id)).first()
        return hotel

    def list_hotels_by_city(self, city: str) -> list[Hotel]:
        hotels = self.session.scalars(
            select(Hotel).where(Hotel.city == city.strip().lower())
        ).all()
        return list(hotels)

    def get_hotel_by_name(self, name:str) -> list[Hotel] | None:
        hotel = self.session.scalars(
            select(Hotel).where(Hotel.name.ilike(f"%{name.strip().lower()}%"))
        ).all()
        return list(hotel)

    def list_hotels_by_stars(self, stars_from: float, stars_to: float) -> list[Hotel]:
        hotels = self.session.scalars(
            select(Hotel).where(Hotel.stars >= stars_from, Hotel.stars <= stars_to)
        ).all()
        return list(hotels)

    def list_hotels_by_filter(self, hotel_filters: dict) -> list[Hotel]:
        stars_from = hotel_filters.get("stars_from")
        stars_to = hotel_filters.get("stars_to")
        city = hotel_filters.get("city")

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


