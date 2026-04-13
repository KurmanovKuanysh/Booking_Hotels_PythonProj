from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.schemas.booking import BookingRead, BookingEditAdmin
from backend.app.schemas.hotel import HotelRead, HotelBase, HotelEdit
from backend.app.schemas.room import RoomRead, RoomEdit, RoomCreate
from backend.app.schemas.user import UserRead, UserCreate, UserEditAdmin, UserRegister

from backend.app.api.deps import get_db, get_current_user_admin
from backend.app.core.exceptions import NoPermissionRole, DuplicateEmailError

from backend.app.services.booking import BookingService
from backend.app.services.hotel import HotelService
from backend.app.services.room import RoomService
from backend.app.services.token import TokenService
from backend.app.services.user import UserService

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(get_current_user_admin)])

@router.post("/auth/register-admin", status_code=201)
def create_user_account(
        user_data: UserRegister,
        db: Session = Depends(get_db),
        admin: UserRead = Depends(get_current_user_admin)
):
    service = UserService(db)
    if admin.role != "S-ADMIN":
        raise NoPermissionRole
    if service.find_user_by_email(str(user_data.email)) is not None:
        raise DuplicateEmailError  # BAD REQUEST

    new_user = service.register_user(
        name=user_data.name,
        email=str(user_data.email),
        password=user_data.password,
        role="ADMIN"
    )
    return new_user
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
@router.delete("/users/{user_id}/delete-cascade", status_code=204)
def delete_user_cascade_force_admin(
        user_id: int,
        db: Session = Depends(get_db),
        admin: UserRead = Depends(get_current_user_admin)
):
    if admin.role != "S-ADMIN":
        raise NoPermissionRole
    service_user = UserService(db)
    service_booking = BookingService(db)
    try:
        service_user.get_user_by_id(user_id)
        have_bookings = service_booking.get_bookings_by_user_id(user_id)
        if have_bookings:
            for booking in have_bookings:
                service_booking.delete_booking_cascade_admin(booking.id)
        service_user.delete_user(user_id)
    except Exception as e:
        raise e
#USEREND=================================================


#ROOMS=================================================
@router.get("/rooms", response_model=list[RoomRead])
def get_rooms(db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.get_all_rooms()
@router.get("/rooms/{room_id}", response_model=RoomRead)
def get_room_by_id(room_id:int, db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.get_room_by_id(room_id)
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
@router.patch("/bookings/update-all-status", response_model=list[BookingRead])
def update_booking_statuses_to_completed_admin(db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.check_update_completed_bookings()
@router.patch("/bookings/{booking_id}/edit", response_model=BookingRead)
def edit_booking_admin_side(
        booking_id: int,
        edit: BookingEditAdmin,
        db: Session = Depends(get_db),
        user: UserRead = Depends(get_current_user_admin)
):
    service = BookingService(db)
    return service.edit_booking_admin_side(
        user=user,
        booking_id=booking_id,
        edit=edit
    )
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
@router.get("/bookings/{booking_id}", response_model=BookingRead)
def get_booking_by_id(
    booking_id: int,
    db: Session = Depends(get_db)
):
    service = BookingService(db)
    return service.get_booking_by_id(booking_id)
@router.get("/bookings/{booking_id}/status", response_model=str)
def get_booking_status(
        booking_id: int,
        db: Session = Depends(get_db)
):
    service = BookingService(db)
    return service.get_booking_status(booking_id)
@router.get("/bookings/user/{user_id}", response_model=list[BookingRead])
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    service = BookingService(db)
    return service.get_bookings_by_user_id(user_id)

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
@router.get("/hotels/{hotel_id}", response_model=HotelRead)
def get_hotel_by_id(hotel_id: int, db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.get_hotel_by_id(hotel_id)
@router.delete("/hotels/{hotel_id}", status_code=204)
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    service = HotelService(db)
    return service.delete_hotel(hotel_id)
#HOTELEND=================================================


#TOKEN
@router.post("/token/clean-up", response_model=int)
def token_clean_up(db: Session = Depends(get_db)):
    token_service = TokenService(db)
    return token_service.clean_up_expired_tokens()
#TOKENEND