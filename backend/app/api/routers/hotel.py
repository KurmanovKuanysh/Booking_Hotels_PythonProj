from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.services.hotel import HotelService
from backend.app.api.deps import get_db
from backend.app.schemas.hotel import HotelRead, HotelBase, HotelEdit
from backend.app.models.filter import FHotel

router = APIRouter(tags=["Hotels"])


@router.get("/hotels", response_model=list[HotelRead])
def get_hotels(db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.get_hotels()

@router.get("/hotels/search/address", response_model=list[HotelRead])
def get_hotels_by_address(address: str, db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.get_hotels_by_address(address)

@router.get("/hotels/search/name", response_model=list[HotelRead])
def get_hotels_by_name(name: str, db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.get_hotels_by_name(name)

@router.get("/hotels/filter", response_model=list[HotelRead])
def get_hotels_by_filter(
        filters: FHotel = Depends(),
        db: Session = Depends(get_db)
):
    service = HotelService(db)
    return service.list_hotels_by_filter(
        filters
    )
@router.get("/hotels/{hotel_id}", response_model=HotelRead)
def get_hotel_by_id(hotel_id: int, db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.get_hotel_by_id(hotel_id)
