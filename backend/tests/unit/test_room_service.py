import pytest

from backend.app.models import Hotel, RoomType
from backend.app.services.room import RoomService
from backend.app.services.hotel import HotelService
from backend.app.models.room import Room

from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.app.services.room_type import RoomTypeService

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
def room_type_one(session: Session):
    service = RoomTypeService(session)

    return service.add_type("Deluxe")

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



def test_add_room_return_room(session: Session, hotel_one, room_type_one):
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
    result = session.scalars(
        select(Room)
        .where(Room.id == room.id)
    ).one_or_none()
    assert result == room

def test_add_room_return_none(session: Session, room_one: Room):
    service = RoomService(session)

    room = service.get_room_by_id(-1)
    assert room is None

def test_add_room_duplicate_room_number(session: Session, room_one: Room, hotel_one, room_type_one):
    service = RoomService(session)
    with pytest.raises(ValueError, match="Room number already exists on Rooms"):
        service.add_room(
            h_id=hotel_one.id,
            room_number="100",
            r_t_id=room_type_one.id,
            capacity=2,
            price_per_day=100,
            floor=1,
            description="Test Room"
        )

def test_get_rooms_return_rooms(session: Session, room_one: Room):
    service = RoomService(session)
    rooms = service.get_rooms()

    assert rooms == [room_one]

def test_get_rooms_return_none(session: Session):
    service = RoomService(session)
    room = service.get_rooms()

    assert room == []

def test_get_room_by_id_return_room(session: Session, room_one: Room):
    service = RoomService(session)
    room = service.get_room_by_id(room_one.id)

    assert room.room_number == room_one.room_number

def test_get_room_by_id_return_none(session: Session):
    service = RoomService(session)
    room = service.get_room_by_id(-1)

    assert room is None


