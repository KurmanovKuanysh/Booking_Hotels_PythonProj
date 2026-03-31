from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.schemas.booking import BookingRead
from backend.app.schemas.hotel import HotelRead, HotelBase, HotelEdit
from backend.app.schemas.room import RoomRead, RoomEdit, RoomCreate
from backend.app.schemas.user import UserRead, UserCreate, UserEditAdmin
from backend.app.api.deps import get_db, get_current_user_admin, get_current_user
from backend.app.services.booking import BookingService
from backend.app.services.hotel import HotelService
from backend.app.services.room import RoomService
from backend.app.services.user import UserService

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(get_current_user_admin)])

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
@router.patch("/users/{user_id}/edit/force", response_model=UserRead)
def edit_user_force_admin(
        user_id: int,
        data: UserEditAdmin,
        db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.edit_user_admin(user_id, data)
#USEREND=================================================


#ROOMS=================================================
@router.post("/hotels/{hotel_id}/rooms", response_model=RoomRead)
def create_new_room(
        hotel_id: int,
        room: RoomCreate,
        db: Session = Depends(get_db)
):
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
@router.get("/bookings", response_model=list[BookingRead])
def get_bookings(
    db: Session = Depends(get_db)
):
    service = BookingService(db)
    return service.get_all_bookings()
@router.patch("/bookings/{booking_id}/status", response_model=bool)
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
@router.patch("/bookings/update-all-status", response_model=list[BookingRead])
def update_booking_statuses_to_completed_admin(db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.check_update_completed_bookings()
@router.delete("/bookings/{booking_id}", response_model=bool)
def delete_booking(
        booking_id: int,
        db: Session = Depends(get_db)
) -> bool:
    service = BookingService(db)

    booking = service.get_booking_by_id(booking_id)
    can_delete = booking.status in ["cancelled", "completed"]

    if not can_delete:
        raise HTTPException(status_code=403, detail="Not Allowed")
    return service.delete_booking(booking_id)

#BOOKINGEND=================================================


#HOTEL=================================================
@router.post("/hotels", response_model=HotelRead)
def create_hotel(
        hotel: HotelBase,
        db: Session = Depends(get_db)
):
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


