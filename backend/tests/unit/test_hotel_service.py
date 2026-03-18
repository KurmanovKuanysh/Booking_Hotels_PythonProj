import pytest
from fastapi import HTTPException

from backend.app.services.hotel import HotelService
from backend.app.models.hotel import Hotel
from backend.app.models.booking import Booking
from backend.app.models.room import Room
from backend.app.models.room_type import RoomType
from backend.app.models.user import User
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.app.services.room import RoomService
from backend.app.services.room_type import RoomTypeService
from backend.app.services.user import UserService

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
@pytest.fixture
def hotel_two(session: Session):
    service = HotelService(session)

    hotel = service.add_hotel(
        name="Test Hotel2",
        city="Test City2",
        stars=4.5,
        address="123 Test Street2"
    )
    return hotel
@pytest.fixture
def booking_one(session: Session, room_one, user_one):
    booking = Booking(
        r_id = room_one.id,
        check_in = date.today() + timedelta(days=3),
        check_out= date.today() + timedelta(days=4),
        status = "confirmed",
        user_id = user_one.id
    )
    session.add(booking)
    session.commit()
    session.refresh(booking)

    return booking
@pytest.fixture
def room_one(session: Session, hotel_one, room_type_one):
    service = RoomService(session)
    room = service.add_room(
        h_id=hotel_one.id,
        room_number="100",
        r_t_id=room_type_one.id,
        capacity=2,
        price_per_day=100,
        floor=1,
        description="Test Room"
    )
    return room

@pytest.fixture
def room_type_one(session: Session):
    service = RoomTypeService(session)

    return service.add_type("Deluxe")

@pytest.fixture
def user_one(session: Session):
    service = UserService(session)
    user = service.add_user(
        name="Test User",
        email="testuser@gmail.com",
        password="password",
        role="USER"
    )
    return user

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

    with pytest.raises(HTTPException, match="Hotel with this name already exists"):
        service.add_hotel(
            name="Test Hotel",
            city="Test City",
            stars=4.5,
            address="123 Test Street"
        )

def test_add_hotel_duplicate_address(session: Session, hotel_one: Hotel):
    service = HotelService(session)

    with pytest.raises(HTTPException, match="Hotel with this address already exists"):
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

def test_get_hotel_by_id_return_none(session: Session, hotel_one: Hotel):
    service = HotelService(session)

    with pytest.raises(HTTPException, match="Hotel not found"):
        service.get_hotel_by_id(hotel_one.id + 1)


def test_edit_hotel_return_edited(session: Session, hotel_one: Hotel):
    service = HotelService(session)

    hotel = service.get_hotel_by_id(hotel_one.id)
    assert hotel.name == "Test Hotel"

    edited_hotel = service.edit_hotel(
        hotel_id=hotel_one.id,
        name="New Name",
        city="Almaty",
        address="Taugul-3 Almaty"
    )

    assert edited_hotel.name == "New Name"
    assert edited_hotel.city == "Almaty"
    assert edited_hotel.address == "Taugul-3 Almaty"

def test_edit_hotel_return_none(session: Session, hotel_one: Hotel, hotel_two: Hotel):
    service = HotelService(session)

    hotel = service.get_hotel_by_id(hotel_one.id)
    assert hotel.id == hotel_one.id

    with pytest.raises(HTTPException, match="Hotel not found"):
        service.edit_hotel(
            hotel_id=hotel_one.id + 10,
            name="New Name",
            city="Almaty",
            address="Taugul-3 Almaty"
        )
    with pytest.raises(HTTPException, match="Hotel name must be at least 3 characters long"):
        service.edit_hotel(
            hotel_id=hotel_one.id,
            name="N",
            city="Almaty",
        )
    with pytest.raises(HTTPException, match="Hotel name must be at most 100 characters long"):
        service.edit_hotel(
            hotel_id=hotel_one.id,
            name = "N"*101
        )
    with pytest.raises(HTTPException, match="Hotel name already exists"):
        service.edit_hotel(
            hotel_id=hotel_one.id,
            name="Test Hotel2"
        )
    with pytest.raises(HTTPException, match="Address must be at least 3 characters long"):
        service.edit_hotel(
            hotel_id=hotel_one.id,
            address="N"
        )
    with pytest.raises(HTTPException, match="Address already exists on Hotels"):
        service.edit_hotel(
            hotel_id=hotel_one.id,
            address="123 Test Street2"
        )
    with pytest.raises(HTTPException, match="Hotel city must be at least 3 characters long"):
        service.edit_hotel(
            hotel_id=hotel_one.id,
            city="N"
        )
    with pytest.raises(HTTPException, match="Hotel city must be at most 100 characters long"):
        service.edit_hotel(
            hotel_id=hotel_one.id,
            city = "N"*101
        )
    with pytest.raises(HTTPException, match="Stars must be between 1 and 5"):
        service.edit_hotel(
            hotel_id=hotel_one.id,
            stars=0
        )
    with pytest.raises(HTTPException, match="Description must be at most 255 characters long"):
        service.edit_hotel(
            hotel_id=hotel_one.id,
            description="N"*256
        )
def test_delete_hotel_return_true(session: Session, hotel_one: Hotel):
    service = HotelService(session)

    hotel = service.get_hotel_by_id(hotel_one.id)
    assert hotel == hotel_one

    service.delete_hotel(hotel_one.id)

    with pytest.raises(HTTPException, match="Hotel not found"):
        service.get_hotel_by_id(hotel_one.id)

def test_delete_hotel_return_false(session: Session, hotel_one: Hotel, booking_one: Booking):
    service = HotelService(session)
    hotel_id = hotel_one.id
    hotel = service.get_hotel_by_id(hotel_one.id)
    assert hotel == hotel_one

    with pytest.raises(HTTPException, match="Hotel not found"):
        service.delete_hotel(hotel_id + 100)
    with pytest.raises(HTTPException, match="Hotel have active booking"):
        service.delete_hotel(hotel_id)



