from datetime import datetime

from pydantic import BaseModel, Field

class ReviewCreate(BaseModel):
    booking_id: int = Field(gt=0)
    rating: int = Field(ge=1, le=5)
    comment: str = Field(min_length=1, max_length=255)

class ReviewRead(BaseModel):
    id: int = Field(gt=0)
    booking_id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    hotel_id: int = Field(gt=0)
    rating: int = Field(ge=1, le=5)
    comment: str = Field(min_length=1, max_length=255)
    created_at: datetime

class ReviewEdit(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    comment: str | None = Field(default=None, min_length=1, max_length=255)