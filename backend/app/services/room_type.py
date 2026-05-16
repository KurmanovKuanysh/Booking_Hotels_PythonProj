from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.models.room_type import RoomType
from backend.app.models.room import Room

class RoomTypeService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_type(self, name: str) -> RoomType:
        room_type = RoomType(
            type_name=name.strip().lower()
        )
        self.session.add(room_type)
        await self.session.commit()
        await self.session.refresh(room_type)
        return room_type

    async def get_types(self, rooms: list[Room]) -> list[RoomType]:
        if not rooms:
            return []
        types_ids = {room.r_t_id for room in rooms}
        stmt = select(RoomType).where(RoomType.id.in_(types_ids))
        return list((await self.session.scalars(stmt)).all())

    async def get_type_by_id(self, type_id: int) -> RoomType | None:
        return await self.session.scalar(select(RoomType).where(RoomType.id == type_id))