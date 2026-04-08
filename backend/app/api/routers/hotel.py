from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.services.hotel import HotelService
from backend.app.api.deps import get_db
from backend.app.schemas.hotel import HotelRead
from backend.app.models.filter import FHotel

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

@router.get("/hotels/filter", response_model=list[HotelRead])
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
