import pytest
from backend.app.services.hotel import HotelService
from backend.app.models.hotel import Hotel
from sqlalchemy.orm import Session
from sqlalchemy import select

@pytest.fixture
def hotel_one(session: Session):
    service = HotelService(session)

    hotel = service.add_hotel(
        name="Test Hotel",
        city="Test City",
        stars=4.5,
        address="123 Test Street"
    )

    return hotel


def test_add_hotel(session: Session):
    service = HotelService(session)

    hotels = session.scalars(select(Hotel)).all()
    assert hotels == []

    hotel = service.add_hotel(
        name="Test Hotel",
        city="Test City",
        stars=4.5,
        address="123 Test Street"
    )
    result = session.scalars(
        select(Hotel)
        .where(Hotel.id == hotel.id)
    ).one_or_none()

    assert result == hotel

def test_add_hotel_duplicate_name(session: Session, hotel_one: Hotel):
    service = HotelService(session)
    pass