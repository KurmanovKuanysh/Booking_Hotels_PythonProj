from pydantic import BaseModel, Field, ConfigDict

class RoomCreate(BaseModel):
    room_number: str = Field(min_length=1, max_length=10)
    r_t_id: int = Field(gt=0)
    capacity: int = Field(ge=1)
    price_per_day: float = Field(gt=0)
    floor: int = Field(ge=1)
    description: str | None = None

class RoomRead(BaseModel):
    id: int
    room_number: str
    r_t_id: int
    capacity: int
    price_per_day: float
    floor: int
    description: str | None

    model_config = ConfigDict(from_attributes=True)

class RoomEdit(BaseModel):
    room_number: str | None = Field(default=None, min_length=1, max_length=10)
    r_t_id: int | None = Field(default=None, gt=0)
    capacity: int | None = Field(default=None, ge=1)
    price_per_day: float | None =Field(default=None, gt=0)
    floor: int | None = Field(default=None, ge=1)
    description: str | None = Field(default=None,min_length=1,max_length=255)