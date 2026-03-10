from sqlalchemy.orm import Session
from sqlalchemy import select, update

from backend.app.models.booking import Booking
from backend.app.models.room import Room
from backend.app.models.room_type import RoomType
from datetime import date


class RoomService:
    def __init__(self, session: Session):
        self.session = session

    def add_room(self, h_id:int,room_number:str, r_t_id:int, price_per_day:float, capacity:int, floor:int):
        room = Room(
            h_id=h_id,
            room_number=room_number,
            r_t_id=r_t_id,
            capacity=capacity,
            price_per_day=price_per_day,
            floor=floor
        )
        self.session.add(room)
        self.session.commit()
        self.session.refresh(room)
        return room

    def delete_room(self, r_id:int):
        try:
            self.session.execute(
                update(Room)
                .where(Room.id == r_id)
                .values(is_deleted=True)
            )
            self.session.commit()
            self.session.refresh(Room)
        except Exception as e:
            print(f"Error deleting room: {e}")
            raise

    def list_rooms_by_hotel_id(self, h_id:int) -> list[Room]:
        return list(self.session.scalars(select(Room).where(Room.h_id == h_id)).all())

    def get_room_by_id(self, r_id:int) -> Room | None:
        return self.session.scalars(select(Room).where(Room.id == r_id)).first()

    def list_rooms_by_price(self, min_price: float, max_price: float) -> list[Room]:
        return list(self.session.scalars(
            select(Room).where(
                Room.price_per_day >= min_price,
                Room.price_per_day <= max_price )
            ).all()
        )

    def list_rooms_by_type(self, room_type:str) -> list[Room]:
        return list(self.session.scalars(
            select(Room)
            .join(RoomType, RoomType.id == Room.r_t_id)
            .where(RoomType.type_name == room_type)
            ).all()
        )

    def list_rooms_by_capacity(self, person:int) -> list[Room]:
        return list(self.session.scalars(
            select(Room).where(Room.capacity >= person)
            ).all()
        )

    def is_room_available(self, r_id:int, check_in: date, check_out: date) -> bool:
        booking = self.session.scalars(
            select(Booking)
            .where(
                Booking.r_id == r_id,
                Booking.status.in_(["confirmed", "pending"]),
                Booking.check_out >= check_in,
                Booking.check_in <= check_out
            )
        ).first()
        return booking is None

    def get_price_range(self, rooms:list[Room]) -> dict[str,float]:
        min_price = min(room.price_per_day for room in rooms)
        max_price = max(room.price_per_day for room in rooms)
        return {
            "min": float(min_price),
            "max": float(max_price),
        }

    def get_rooms_by_filter(self,h_id: int , r_filter: dict) -> list[Room]:
        capacity = r_filter.get("capacity")
        price_from = r_filter.get("price_from")
        price_to = r_filter.get("price_to")
        room_type = r_filter.get("room_type")

        rooms = select(Room).where(Room.h_id == h_id)

        if capacity:
            rooms = rooms.where(Room.capacity >= int(capacity))
        if price_from:
            rooms = rooms.where(Room.price_per_day >= float(price_from))
        if price_to:
            rooms = rooms.where(Room.price_per_day <= float(price_to))
        if room_type:
            rooms = rooms.join(RoomType, RoomType.id == Room.r_t_id).where(RoomType.type_name == room_type)

        return list(self.session.scalars(rooms).all())
