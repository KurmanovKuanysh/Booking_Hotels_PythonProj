from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.schemas.room import RoomRead
from backend.app.services.hotel import HotelService
from backend.app.api.deps import get_db
from backend.app.schemas.hotel import HotelRead
from backend.app.models.filter import FHotel, FRoom
from backend.app.services.room import RoomService

router = APIRouter(tags=["Hotels"])


@router.get("/hotels", response_model=list[HotelRead])
def get_hotels(
        page: int = 1,
        size: int = 5,
        db: Session = Depends(get_db)
):
    offset = (page - 1) * size
    service = HotelService(db)
    return service.get_hotels(limit=size,offset=offset)

@router.get("/hotels/search/address", response_model=list[HotelRead])
def get_hotels_by_address(address: str, db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.get_hotels_by_address(address)

@router.get("/hotels/search/name", response_model=list[HotelRead])
def get_hotels_by_name(name: str, db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.get_hotels_by_name(name)

@router.get("/hotels/search/filter", response_model=list[HotelRead])
def get_hotels_by_filter(
        filters: FHotel = Depends(),
        db: Session = Depends(get_db)
):
    service = HotelService(db)
    return service.list_hotels_by_filter(
        filters
    )

@router.get("/hotels/popular", response_model=list[HotelRead])
def get_popular_hotels(
        limit: int = 5,
        db: Session = Depends(get_db)
):
    service = HotelService(db)
    return service.get_popular_hotels(limit=limit)

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
