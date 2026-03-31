from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.models.filter import FRoom
from backend.app.services.room import RoomService
from backend.app.api.deps import get_db
from backend.app.schemas.room import RoomRead, RoomEdit
from datetime import date

router = APIRouter(tags=["Rooms"])
@router.get("/rooms", response_model=list[RoomRead])
def get_rooms(db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.get_all_rooms()
@router.get("/rooms/{room_id}", response_model=RoomRead)
def get_room_by_id(room_id:int, db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.get_room_by_id(room_id)
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
        check_in: date,
        check_out: date,
        db: Session = Depends(get_db)
):
    service = RoomService(db)
    rooms = service.list_rooms_by_hotel_id(hotel_id)
    return service.get_available_rooms_hotel_dates(
        rooms=rooms,
        check_in=check_in,
        check_out=check_out
    )