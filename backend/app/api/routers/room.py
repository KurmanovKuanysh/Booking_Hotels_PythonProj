from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.services.room import RoomService
from backend.app.api.deps import get_db
from backend.app.schemas.room import RoomBase, RoomRead

router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.post("/{hotel_id}/rooms", response_model=RoomRead)
def create_room(hotel_id:int, room: RoomBase, db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.add_room(
        h_id=hotel_id,
        room_number=room.room_number,
        r_t_id=room.r_t_id,
        capacity=room.capacity,
        price_per_day=room.price_per_day,
        floor=room.floor,
        description=room.description
    )
@router.delete("/rooms/{room_id}", response_model=bool)
def delete_room(room_id:int, db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.delete_room(room_id)

@router.get("/rooms", response_model=list[RoomRead])
def get_rooms(db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.get_rooms()
@router.get("/{hotel_id}/rooms", response_model=list[RoomRead])
def get_rooms_by_hotel_id(hotel_id:int, db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.list_rooms_by_hotel_id(hotel_id)


@router.get("/rooms/{room_id}", response_model=RoomRead)
def get_room_by_id(room_id:int, db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.get_room_by_id(room_id)

@router.get("/rooms/by_price", response_model=list[RoomRead])
def get_rooms_by_price_range(min_price:float, max_price:float, db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.list_rooms_by_price(min_price, max_price)
@router.get("/rooms/by_type", response_model=list[RoomRead])
def get_rooms_by_type(room_type:str, db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.list_rooms_by_type(room_type)

@router.get("/rooms/by_capacity", response_model=list[RoomRead])
def get_rooms_by_capacity(capacity:int, db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.list_rooms_by_capacity(capacity)

@router.get("/{hotel_id}/rooms/by_filter", response_model=list[RoomRead])
def get_rooms_by_filter(
    hotel_id: int,
    capacity: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    room_type: str | None = None,
    db: Session = Depends(get_db)
):
    service = RoomService(db)
    return service.get_rooms_by_filter(
        hotel_id=hotel_id,
        capacity=capacity,
        min_price=min_price,
        max_price=max_price,
        room_type=room_type
    )
@router.patch("/{hotel_id}/rooms/{room_id}/edit", response_model=RoomRead)
def edit_room(
        hotel_id:int,
        room_id:int,
        room_number:str | None = None,
        r_t_id:int | None = None,
        capacity:int | None = None,
        price_per_day:float | None = None,
        floor:int | None = None,
        description:str | None = None,
        db: Session = Depends(get_db)
):
    service = RoomService(db)
    return service.edit_room(
        hotel_id=hotel_id,
        room_id=room_id,
        room_number=room_number,
        r_t_id=r_t_id,
        capacity=capacity,
        price_per_day=price_per_day,
        floor=floor,
        description=description
    )