from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.schemas.booking import BookingRead
from backend.app.schemas.hotel import HotelRead, HotelBase, HotelEdit
from backend.app.schemas.room import RoomRead, RoomEdit
from backend.app.schemas.user import UserRead, UserCreate
from backend.app.api.deps import get_db
from backend.app.services.booking import BookingService
from backend.app.services.hotel import HotelService
from backend.app.services.room import RoomService
from backend.app.services.user import UserService

router = APIRouter(prefix="/admin", tags=["Admin"])

#USER=================================================
@router.post("/users", response_model=UserRead)
def create_user(
        user: UserCreate,
        db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.add_user(
        user.name,
        user.email,
        user.password,
        user.role
    )
@router.get("/users/by-email", response_model=UserRead)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_user_by_email(email)
@router.get("/users/by-name", response_model=list[UserRead])
def get_user_by_name(name: str, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_users_by_name(name)
@router.get("/users", response_model=list[UserRead])
def get_all_users(db: Session = Depends(get_db) ):
    service = UserService(db)
    return service.get_users()
@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.delete_user(user_id)
@router.get("/users/{user_id}", response_model=UserRead)
def get_user_by_id(user_id:int , db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_user_by_id(user_id)
#USEREND=================================================


#ROOMS=================================================
@router.post("/hotels/{hotel_id}/rooms", response_model=RoomRead)
def create_new_room(hotel_id: int, room: RoomRead, db: Session = Depends(get_db)):
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
@router.patch("/hotels/{hotel_id}/rooms/{room_id}", response_model=RoomRead)
def edit_room(
        hotel_id:int,
        room_id:int,
        room : RoomEdit,
        db: Session = Depends(get_db)
):
    service = RoomService(db)
    return service.edit_room(
        hotel_id=hotel_id,
        room_id=room_id,
        room_number=room.room_number,
        r_t_id=room.r_t_id,
        capacity=room.capacity,
        price_per_day=room.price_per_day,
        floor=room.floor,
        description=room.description
    )

@router.delete("/rooms/{room_id}", status_code=204)
def delete_room(room_id:int, db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.delete_room(room_id)
#ROOMSEND=================================================


#BOOKING=================================================
@router.patch("/admin/{booking_id}/status", response_model=bool)
def update_booking_status(
        booking_id: int,
        status: str,
        db: Session = Depends(get_db)
):
    service = BookingService(db)
    return service.update_booking_status(
        booking_id=booking_id,
        new_status=status
    )
@router.patch("/admin/update-all-status", response_model=list[BookingRead])
def update_booking_statuses_to_completed_admin(db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.check_update_completed_bookings()
#BOOKINGEND=================================================


#HOTEL=================================================
@router.post("/hotels", response_model=HotelRead)
def create_hotel(hotel: HotelBase, db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.add_hotel(
        name=hotel.name,
        city=hotel.city,
        stars=hotel.stars,
        address=hotel.address,
        description=hotel.description
    )
@router.patch("/hotels/{hotel_id}/edit", response_model=HotelRead)
def edit_hotel(
        hotel_id: int,
        data: HotelEdit,
        db: Session = Depends(get_db)
):
    service = HotelService(db)
    return service.edit_hotel(
        hotel_id=hotel_id,
        name=data.name,
        city=data.city,
        address=data.address,
        stars=data.stars,
        description=data.description
    )
@router.delete("/hotels/{hotel_id}", status_code=204)
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.delete_hotel(hotel_id)
#HOTELEND=================================================


