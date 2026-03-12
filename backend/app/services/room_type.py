from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.app.models.room_type import RoomType
from backend.app.models.room import Room

class RoomTypeService:
    def __init__(self, session: Session):
        self.session = session

    def add_type(self, name: str) -> RoomType:
        room_type = RoomType(
            type_name=name.strip().lower()
        )
        self.session.add(room_type)
        self.session.commit()
        self.session.refresh(room_type)
        return room_type

    def get_types(self, rooms: list[Room]) -> list[RoomType]:
        if not rooms:
            return []
        types_ids = {room.r_t_id for room in rooms}
        stmt = select(RoomType).where(RoomType.id.in_(types_ids))
        return list(self.session.scalars(stmt).all())

    def get_type_by_id(self, type_id: int) -> RoomType | None:
        return self.session.scalars(select(RoomType).where(RoomType.id == type_id)).first()