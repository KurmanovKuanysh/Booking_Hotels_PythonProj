from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.exceptions import NotFoundBookedRoomsError
from backend.app.models.filter import FRoom
from backend.app.schemas.user import UserRead
from backend.app.services.room import RoomService
from backend.app.api.deps import get_db, get_current_user
from backend.app.schemas.room import RoomRead, RoomAvailable, RoomDate
from datetime import date

router = APIRouter(tags=["Rooms"])
@router.get("/rooms/my-rooms", response_model=list[RoomRead])
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
        check_in: date = date.today(),
        check_out: date | None = None,
        guests: int = 1,
        db: Session = Depends(get_db),
):
    service = RoomService(db)
    return service.get_all_available_rooms(
        city=city,
        check_in=check_in,
        check_out=check_out,
        guests=guests
    )

@router.post("/rooms/{room_id}/check-availability", response_model=bool)
def check_availability_single_room(
        room_id: int,
        data: RoomDate,
        db: Session = Depends(get_db)
):
    service = RoomService(db)
    return service.is_room_available(
        room_id=room_id,
        data=data
    )