import pytest
from backend.app.services.booking import BookingService
from backend.app.services.hotel import HotelService
from backend.app.services.room import RoomService
from backend.app.services.room_type import RoomTypeService
from backend.app.services.user import UserService
from backend.app.models.booking import Booking

from sqlalchemy.orm import Session
from sqlalchemy import select

from datetime import date, timedelta

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

def test_add_booking_return_booking(session: Session, room_one, user_one):
    service = BookingService(session)

    booking = service.create_new_booking(
        r_id = room_one.id,
        check_in = date.today() + timedelta(days=3),
        check_out= date.today() + timedelta(days=4),
        status = "confirmed",
        user_id = user_one.id
    )
    result = session.scalar(
        select(Booking)
        .where(Booking.id == booking.id)
    )

    assert result == booking

def test_get_booking_by_id_return_booking(session: Session, booking_one):
    service = BookingService(session)

    booking = service.get_booking_by_id(booking_one.id)
    assert booking == booking_one

def test_get_booking_by_id_return_none(session: Session):
    service = BookingService(session)

    booking = service.get_booking_by_id(-1)
    assert booking is None

def test_edit_booking_return_booking(session: Session, booking_one):
    service = BookingService(session)

    booking = service.get_booking_by_id(booking_one.id)
    assert booking.status == "confirmed"
    assert booking.check_in == date.today() + timedelta(days=3)

    edit = {
        "id": booking_one.id,
        "check_in": date.today() + timedelta(days=4),
        "check_out": date.today() + timedelta(days=5),
        "status": "cancelled"
    }

    edited_booking = service.edit_booking(
        booking_id=edit["id"],
        check_in=edit["check_in"],
        check_out=edit["check_out"],
        status=edit["status"]
    )

    assert edited_booking.check_in == date.today() + timedelta(days=4)
    assert edited_booking.check_out == date.today() + timedelta(days=5)
    assert edited_booking.status == "cancelled"
