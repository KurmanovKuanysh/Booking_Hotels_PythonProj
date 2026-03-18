from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.services.hotel import HotelService
from backend.app.api.deps import get_db
from backend.app.schemas.hotel import HotelRead, HotelBase

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.post("/", response_model=HotelRead)
def create_hotel(hotel: HotelBase, db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.add_hotel(
        name=hotel.name,
        city=hotel.city,
        stars=hotel.stars,
        address=hotel.address,
        description=hotel.description
    )

@router.get("/", response_model=list[HotelRead])
def get_hotels(db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.get_hotels()

@router.get("/by_city", response_model=list[HotelRead])
def get_hotels_by_city(city: str, db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.list_hotels_by_city(city)
@router.get("/by_address", response_model=HotelRead)
def get_hotel_by_address(address: str, db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.get_hotel_by_address(address)

@router.get("/by_name", response_model=list[HotelRead])
def get_hotels_by_name(name: str, db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.get_hotel_by_name(name)
@router.get("/by_stars", response_model=list[HotelRead])
def get_hotel_by_stars(stars_from: float, stars_to: float, db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.list_hotels_by_stars(stars_from, stars_to)
@router.get("/by_filter", response_model=list[HotelRead])
def get_hotels_by_filter(
        stars_from: float | float = 1,
        stars_to: float | float = 5,
        city: str | None = None,
        db: Session = Depends(get_db)
):
    service = HotelService(db)
    return service.list_hotels_by_filter(
        stars_from=stars_from,
        stars_to=stars_to,
        city=city
    )
@router.patch("/{hotel_id}/edit", response_model=HotelRead)
def edit_hotel(
        hotel_id: int,
        name: str | None = None,
        city: str | None = None,
        address: str | None = None,
        stars: float | None = None,
        description: str | None = None,
        db: Session = Depends(get_db)
):
    service = HotelService(db)
    return service.edit_hotel(
        hotel_id=hotel_id,
        name=name,
        city=city,
        address=address,
        stars=stars,
        description=description
    )
@router.get("/{hotel_id}", response_model=HotelRead)
def get_hotel_by_id(hotel_id: int, db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.get_hotel_by_id(hotel_id)
@router.delete("/{hotel_id}", response_model=bool)
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.delete_hotel(hotel_id)

