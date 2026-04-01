from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import date

from backend.app.core.exceptions import DatesConflictError


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

class RoomAvailable(BaseModel):
    city: str | None = Field(default=None, min_length=3, max_length=100)
    check_in: date | None = Field(default=None)
    check_out: date | None = Field(default=None)
    guests: int | None = Field(default=None, ge=1)

    @model_validator(mode='after')
    def check_dates_conflict(self):
        if self.check_in and self.check_out and self.check_in > self.check_out:
            raise DatesConflictError
        return self

class RoomDate(BaseModel):
    check_in: date
    check_out: date

    @model_validator(mode='after')
    def check_dates_conflict(self):
        if self.check_in and self.check_out and self.check_in > self.check_out:
            raise DatesConflictError
        return self
