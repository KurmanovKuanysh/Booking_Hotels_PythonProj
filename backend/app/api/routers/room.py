from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.exceptions import NotFoundBookedRoomsError
from backend.app.models.filter import FRoom
from backend.app.schemas.user import UserRead
from backend.app.services.room import RoomService
from backend.app.api.deps import get_db, get_current_user
from backend.app.schemas.room import RoomRead
from datetime import datetime

router = APIRouter(tags=["Rooms"])
@router.get("/hotels/{hotel_id}/rooms", response_model=list[RoomRead])
def get_rooms_by_filter(
        hotel_id: int,
        filters: FRoom = Depends(),
        db: Session = Depends(get_db)
):
    service = RoomService(db)
    return service.get_rooms_by_filter(
        hotel_id = hotel_id,
        filters=filters
    )
@router.get("/hotels/{hotel_id}/rooms/available", response_model=list[RoomRead])
def get_available_rooms_by_hotel_dates(
        hotel_id: int,
        check_in: datetime,
        check_out: datetime,
        db: Session = Depends(get_db)
):
    service = RoomService(db)
    rooms = service.list_rooms_by_hotel_id(hotel_id)
    return service.get_available_rooms_hotel_dates(
        rooms=rooms,
        check_in=check_in,
        check_out=check_out
    )

@router.get("/rooms/my-booked-rooms", response_model=list[RoomRead])
def get_user_rooms(
        user: UserRead = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    service = RoomService(db)
    booked_rooms = service.get_all_booked_rooms_of_user(user.id)
    if not booked_rooms:
        raise NotFoundBookedRoomsError

    return booked_rooms

@router.get("/rooms/available", response_model=list[RoomRead])
def get_all_available_rooms(
        city: str | None = None,
        check_in: datetime | None = None,
        check_out: datetime | None = None,
        guests: int = 1,
        db: Session = Depends(get_db),
):
    service = RoomService(db)
    if check_in is None:
        check_in = datetime.now()
    return service.get_all_available_rooms(
        city=city,
        check_in=check_in,
        check_out=check_out,
        guests=guests
    )

@router.get("/rooms/{room_id}/check-availability", response_model=bool)
def check_availability_single_room(
        room_id: int,
        check_in: datetime,
        check_out: datetime,
        db: Session = Depends(get_db)
):
    service = RoomService(db)
    return service.is_room_available(
        room_id=room_id,
        check_in=check_in,
        check_out=check_out
    )