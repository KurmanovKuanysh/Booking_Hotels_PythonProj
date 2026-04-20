from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict, computed_field


class HotelCreate(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    city: str = Field(min_length=3, max_length=100)
    address: str = Field(min_length=3, max_length=255)
    stars: int = Field(ge=1, le=5)
    description: str | None = None

class HotelRead(BaseModel):
    id: int
    name: str
    city: str
    address: str
    stars: int
    rating_sum: Decimal
    rating_count: int

class HotelEdit(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=120)
    city: str | None = Field(default=None, min_length=3, max_length=100)
    address: str | None = Field(default=None, min_length=3, max_length=255)
    stars: int | None = Field(default=None, ge=1, le=5)
    description: str | None = Field(default=None, max_length=500)

