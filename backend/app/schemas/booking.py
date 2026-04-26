from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict, model_validator

from backend.app.core.exceptions import DatesConflictError
from backend.app.models.booking import Status
from datetime import datetime


class BookingCreate(BaseModel):
    r_id: int = Field(gt=0)
    check_in: datetime
    check_out: datetime
    guest_count: int = Field(default=1, ge=1)

    @model_validator(mode='after')
    def check_dates_conflict(self):
        if self.check_in and self.check_out and self.check_in > self.check_out:
            raise DatesConflictError
        return self


class BookingRead(BaseModel):
    id: int = Field(gt=0)
    r_id: int
    check_in: datetime
    check_out: datetime
    status: Status
    user_id: int
    total_price: float

    model_config = ConfigDict(from_attributes=True)

class BookingEdit(BaseModel):
    r_id: int | None = Field(default=None, gt=0)
    check_in: datetime | None = Field(default=None)
    check_out: datetime | None = Field(default=None)

class BookingCancelResponse(BaseModel):
    message: str
    penalty: Decimal
    refund: Decimal

class BookingEditAdmin(BookingEdit):
    status: Status | None = None
    total_price: float | None = Field(default=None, gt=0)
    user_id: int | None = Field(default=None, gt=0)

class BookingStatusUpdate(BaseModel):
    status: Status