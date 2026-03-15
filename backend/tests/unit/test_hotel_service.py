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

    with pytest.raises(ValueError, match="Hotel with this name already exists"):
        service.add_hotel(
            name="Test Hotel",
            city="Test City",
            stars=4.5,
            address="123 Test Street"
        )

def test_add_hotel_duplicate_address(session: Session, hotel_one: Hotel):
    service = HotelService(session)

    with pytest.raises(ValueError, match="Hotel with this address already exists"):
        service.add_hotel(
            name="Test Hotel2",
            city="Test City2",
            stars=4.5,
            address="123 Test Street"
        )

def test_get_hotels_return_hotels(session: Session, hotel_one: Hotel):
    service = HotelService(session)

    hotels = service.get_hotels()
    assert hotels == [hotel_one]

def test_get_hotels_return_none(session: Session):
    service = HotelService(session)

    hotels = service.get_hotels()
    assert hotels == []

def test_get_hotel_by_id_return_hotel(session: Session, hotel_one: Hotel):
    service = HotelService(session)

    hotel = service.get_hotel_by_id(hotel_one.id)
    assert hotel == hotel_one

def test_edit_hotel(session: Session, hotel_one: Hotel):
    service = HotelService(session)

    hotel = service.get_hotel_by_id(hotel_one.id)
    assert hotel.name == "Test Hotel"

    edit: dict = {
        "id": hotel_one.id,
        "name": "New Name"
    }
    edited_hotel = service.edit_hotel(edit)

    assert edited_hotel.name == "New Name"