from pydantic import BaseModel, Field, ConfigDict
from datetime import date

class BookingBase(BaseModel):
    r_id: int = Field(gt=0)
    check_in: date
    check_out: date
    status: str = Field(min_length=3, max_length=100)
    total_price: float = Field(gt=0)
    user_id: int = Field(gt=0)

class BookingNew(BaseModel):
    r_id: int = Field(gt=0)
    check_in: date
    check_out: date
    status: str = Field(min_length=3, max_length=100)

class BookingRead(BaseModel):
    id: int = Field(gt=0)
    r_id: int
    check_in: date
    check_out: date
    status: str
    user_id: int
    total_price: float

    model_config = ConfigDict(from_attributes=True)

class BookingEdit(BaseModel):
    r_id: int | None = Field(default=None, gt=0)
    check_in: date | None = Field(default=None)
    check_out: date | None = Field(default=None)

class BookingEditAdmin(BookingEdit):
    status: str | None = Field(default=None, min_length=3, max_length=100)
    total_price: float | None = Field(default=None, gt=0)
    user_id: int | None = Field(default=None, gt=0)