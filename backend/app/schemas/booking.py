from pydantic import BaseModel, Field, ConfigDict, model_validator
from backend.app.models.booking import Status
from datetime import date

class BookingBase(BaseModel):
    r_id: int = Field(gt=0)
    check_in: date
    check_out: date
    status: Status = Field(min_length=3, max_length=100)
    total_price: float = Field(gt=0)
    user_id: int = Field(gt=0)

class BookingNew(BaseModel):
    r_id: int = Field(gt=0)
    check_in: date
    check_out: date
    guest_count: int = Field(ge=1)

class BookingRead(BaseModel):
    id: int = Field(gt=0)
    r_id: int
    check_in: date
    check_out: date
    status: Status
    user_id: int
    total_price: float

    model_config = ConfigDict(from_attributes=True)

class BookingEdit(BaseModel):
    r_id: int | None = Field(default=None, gt=0)
    check_in: date | None = Field(default=None)
    check_out: date | None = Field(default=None)

class EditBookingStatus(BaseModel):
    id: int = Field(gt=0)
    status: Status = Field(min_length=3, max_length=10)


class BookingEditAdmin(BookingEdit):
    status: Status | None = Field(default=None, min_length=3, max_length=100)
    total_price: float | None = Field(default=None, gt=0)
    user_id: int | None = Field(default=None, gt=0)