from pydantic import BaseModel, Field

class RoomBase(BaseModel):
    room_number: str = Field(min_length=1, max_length=10)
    r_t_id: int = Field(gt=0)
    capacity: int = Field(ge=1)
    price_per_day: float = Field(gt=0)
    floor: int = Field(ge=1)
    description: str | None = None

class RoomRead(RoomBase):
    id: int

class RoomEdit(BaseModel):
    room_number: str | None = Field(default=None, min_length=1, max_length=10)
    r_t_id: int | None = Field(default=None, gt=0)
    capacity: int | None = Field(default=None, ge=1)
    price_per_day: float | None =Field(default=None, gt=0)
    floor: int | None = Field(default=None, ge=1)
    description: str | None = Field(default=None,min_length=1,max_length=255)