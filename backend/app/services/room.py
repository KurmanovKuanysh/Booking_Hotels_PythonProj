from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.app.models.booking import Booking
from backend.app.models.room import Room
from backend.app.models.room_type import RoomType
from datetime import date

from fastapi import HTTPException


class RoomService:
    def __init__(self, session: Session):
        self.session = session

    def add_room(
            self,
            h_id:int,
            room_number:str,
            r_t_id:int,
            capacity:int,
            price_per_day:float,
            floor:int,
            description:str
    ):
        if self.session.scalars(
            select(Room)
            .where(Room.room_number == room_number)
        ).all():
            raise HTTPException(status_code=409, detail="Room number already exists on Rooms")
        room = Room(
            h_id=h_id,
            room_number=room_number,
            r_t_id=r_t_id,
            capacity=capacity,
            price_per_day=price_per_day,
            floor=floor,
            description=description
        )
        self.session.add(room)
        self.session.commit()
        self.session.refresh(room)
        return room

    def delete_room(self, r_id:int) -> bool:
        try:
            room = self.get_room_by_id(r_id)
            if not room:
                raise HTTPException(status_code=404, detail="Room not found")
            room_booked = self.session.scalars(
                select(Booking)
                .where(Booking.r_id == r_id,
                       Booking.status.in_(["confirmed", "pending"])
                       )
            ).first()
            if room_booked:
                raise HTTPException(status_code=400, detail="Room has active bookings!")
            self.session.delete(room)
            self.session.commit()
            return True

        except HTTPException:
            self.session.rollback()
            raise
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Error deleting room: {e}")


    def get_rooms(self) -> list[Room]:
        return list(self.session.scalars(select(Room)).all())

    def list_rooms_by_hotel_id(self, h_id:int) -> list[Room]:
        return list(self.session.scalars(select(Room).where(Room.h_id == h_id)).all())

    def get_room_by_id(self, r_id:int) -> Room | None:
        return self.session.scalars(select(Room).where(Room.id == r_id)).first()

    def list_rooms_by_price(self, min_price: float, max_price: float) -> list[Room]:
        return list(
            self.session.scalars(
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

    def get_rooms_by_filter(
            self,
            hotel_id: int,
            capacity: int | None = None,
            min_price: float | None = None,
            max_price: float | None = None,
            room_type: str | None = None
    ) -> list[Room]:
        rooms = select(Room).where(Room.h_id == hotel_id)
        if capacity:
            rooms = rooms.where(Room.capacity >= int(capacity))
        if min_price:
            rooms = rooms.where(Room.price_per_day >= float(min_price))
        if max_price:
            rooms = rooms.where(Room.price_per_day <= float(max_price))
        if room_type:
            rooms = rooms.join(RoomType, RoomType.id == Room.r_t_id).where(RoomType.type_name == room_type)

        return list(self.session.scalars(rooms).all())

    def edit_room(
            self,
            hotel_id:int,
            room_id:int,
            room_number:str | None = None,
            r_t_id:int | None = None,
            capacity:int | None = None,
            price_per_day:float | None = None,
            floor:int | None = None,
            description:str | None = None
    ):
        room = self.get_room_by_id(room_id)
        if room is None:
            raise HTTPException(status_code=404, detail="Room not found")
        if room.h_id != hotel_id:
            raise HTTPException(status_code=404, detail="Room not found in this hotel")
        if room_number is not None:
            same_room_number = self.session.scalar(
                select(Room)
                .where(
                    Room.h_id == hotel_id,
                    Room.room_number == room_number.strip(),
                    Room.id != room.id
                )
            )
            if same_room_number:
                raise HTTPException(status_code=409, detail="Room number already exists in this hotel")
            if len(room_number) > 10:
                raise HTTPException(status_code=400, detail="Room number must be at most 10 characters long")
            room.room_number = room_number.strip()
        if r_t_id is not None:
            room_type = self.session.scalars(select(RoomType).where(RoomType.id == r_t_id)).first()
            if room_type is None:
                raise HTTPException(status_code=404, detail="Room type not found")
            room.r_t_id = r_t_id
        if capacity is not None:
            if capacity < 1:
                raise HTTPException(status_code=400, detail="Capacity must be at least 1")
            room.capacity = capacity
        if price_per_day is not None:
            if price_per_day < 0:
                raise HTTPException(status_code=400, detail="Price per day must be at least 0")
            room.price_per_day = price_per_day
        if floor is not None:
            if floor < 0:
                raise HTTPException(status_code=400, detail="Floor must be at least 0")
            room.floor = floor
        if description is not None:
            if len(description) > 255:
                raise HTTPException(status_code=400, detail="Description must be at most 255 characters long")
            room.description = description
        self.session.commit()
        self.session.refresh(room)
        return room
