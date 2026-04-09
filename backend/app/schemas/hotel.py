from pydantic import BaseModel, Field, ConfigDict


class HotelBase(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    city: str = Field(min_length=3, max_length=100)
    address: str = Field(min_length=3, max_length=255)
    stars: float = Field(ge=0.0, le=5.0)
    description: str | None = None

class HotelRead(HotelBase):
    id: int

class HotelEdit(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=120)
    city: str | None = Field(default=None, min_length=3, max_length=100)
    address: str | None = Field(default=None, min_length=3, max_length=255)
    stars: float | None = Field(default=None, ge=0.0, le=5.0)
    description: str | None = Field(default=None, max_length=255)

class HotelsRoomRead(HotelRead):
    id: int
    room_number: str
    r_t_id: int
    capacity: int
    price_per_day: float
    floor: int
    description: str | None

    model_config = ConfigDict(from_attributes=True)
