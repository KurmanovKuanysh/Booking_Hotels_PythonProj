from pydantic import BaseModel, Field

class RoomBase(BaseModel):
    h_id: int = Field(gt=0)
    room_number: str = Field(min_length=1, max_length=10)
    r_t_id: int = Field(gt=0)
    capacity: int = Field(ge=1)
    price_per_day: float = Field(gt=0)
    floor: int = Field(ge=1)
    description: str | None = None

class RoomCreate(RoomBase):
    pass

class RoomRead(RoomBase):
    id: int

