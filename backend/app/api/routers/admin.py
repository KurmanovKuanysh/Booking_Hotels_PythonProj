from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.models.booking import Status
from backend.app.schemas.booking import BookingRead, BookingEditAdmin
from backend.app.schemas.hotel import HotelRead, HotelEdit, HotelCreate
from backend.app.schemas.room import RoomRead, RoomEdit, RoomCreate
from backend.app.schemas.user import UserRead, UserCreate, UserEditAdmin, UserRegister

from backend.app.api.deps import get_db, get_current_user_admin
from backend.app.core.exceptions import NoPermissionRole, DuplicateEmailError, BookingNotCompletedError

from backend.app.services.booking import BookingService
from backend.app.services.hotel import HotelService
from backend.app.services.room import RoomService
from backend.app.services.token import TokenService
from backend.app.services.user import UserService

from backend.app.api.routers.user import get_user_service
from backend.app.api.routers.hotel import get_hotel_service
from backend.app.api.routers.room import get_room_service
from backend.app.api.routers.booking import get_booking_service
from backend.app.api.routers.auth import get_token_service

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(get_current_user_admin)])

@router.post("/auth/register-admin", status_code=201)
async def create_user_account(
        user_data: UserRegister,
        service: UserService = Depends(get_user_service),
        admin: UserRead = Depends(get_current_user_admin)
):
    if admin.role != "S-ADMIN":
        raise NoPermissionRole
    if await service.find_user_by_email(str(user_data.email)) is not None:
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
async def create_user(
        user: UserCreate,
        service: UserService = Depends(get_user_service),
):
    return await service.add_user(
        user.name,
        user.email,
        user.password,
        user.role
    )
@router.get("/users/by-email", response_model=UserRead)
async def get_user_by_email(
        email: str,
        service: UserService = Depends(get_user_service)
):
    return await service.get_user_by_email(email)

@router.get("/users/by-name", response_model=list[UserRead])
async def get_user_by_name(
        name: str,
        service: UserService = Depends(get_user_service)
):
    return await service.get_users_by_name(name)
@router.get("/users", response_model=list[UserRead])
async def get_all_users(
        service: UserService = Depends(get_user_service)
):
    return await service.get_users()
@router.delete("/users/{user_id}", status_code=204)
async def delete_user(
        user_id: int,
        service: UserService = Depends(get_user_service),
):
    return await service.delete_user(user_id)
@router.get("/users/{user_id}", response_model=UserRead)
async def get_user_by_id(
        user_id:int ,
        service: UserService = Depends(get_user_service)
):
    return await service.get_user_by_id(user_id)
@router.patch("/users/{user_id}/edit/force", response_model=UserRead)
async def edit_user_force_admin(
        user_id: int,
        data: UserEditAdmin,
        service: UserService = Depends(get_user_service),
):
    return await service.edit_user_admin(user_id, data)
@router.delete("/users/{user_id}/delete-cascade", status_code=204)
async def delete_user_cascade_force_admin(
        user_id: int,
        service_user: UserService = Depends(get_user_service),
        service_booking: BookingService = Depends(get_booking_service),
        admin: UserRead = Depends(get_current_user_admin)
):
    if admin.role != "S-ADMIN":
        raise NoPermissionRole
    try:
        await service_user.get_user_by_id(user_id)
        have_bookings = await service_booking.get_bookings_by_user_id(user_id)
        if have_bookings:
            for booking in have_bookings:
                await service_booking.admin_delete_booking_cascade(booking.id)
        await service_user.delete_user(user_id)
    except Exception as e:
        raise e
#USEREND=================================================


#ROOMS=================================================
@router.get("/rooms", response_model=list[RoomRead])
async def get_rooms(
        service: RoomService = Depends(get_room_service)
):
    return await service.get_all_rooms()
@router.get("/rooms/{room_id}", response_model=RoomRead)
async def get_room_by_id(
        room_id:int,
        service: RoomService = Depends(get_room_service)
):
    return await service.get_room_by_id(room_id)
@router.post("/hotels/{hotel_id}/rooms", response_model=RoomRead)
async def create_new_room(
        hotel_id: int,
        room: RoomCreate,
        service: RoomService = Depends(get_room_service),
):
    return await service.add_room(
        h_id=hotel_id,
        room_number=room.room_number,
        r_t_id=room.r_t_id,
        capacity=room.capacity,
        price_per_day=room.price_per_day,
        floor=room.floor,
        description=room.description
    )
@router.patch("/hotels/{hotel_id}/rooms/{room_id}", response_model=RoomRead)
async def edit_room(
        hotel_id:int,
        room_id:int,
        room : RoomEdit,
        service: RoomService = Depends(get_room_service),
):
    return await service.edit_room(
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
async def delete_room(
        room_id:int,
        service: RoomService = Depends(get_room_service),
):
    return await service.delete_room(room_id)
#ROOMSEND=================================================


#BOOKING=================================================
@router.get("/bookings", response_model=list[BookingRead])
async def get_bookings(
    service: BookingService = Depends(get_booking_service),
):
    return await service.get_all_bookings()
@router.patch("/bookings/update-all-status", response_model=list[BookingRead])
async def update_booking_statuses_to_completed_admin(
        service: BookingService = Depends(get_booking_service)
):
    return await service.check_update_completed_bookings()
@router.patch("/bookings/{booking_id}/edit", response_model=BookingRead)
async def edit_booking_admin_side(
        booking_id: int,
        edit: BookingEditAdmin,
        service: BookingService = Depends(get_booking_service),
):
    return await service.edit_booking_admin_side(
        booking_id=booking_id,
        edit=edit
    )
@router.patch("/bookings/{booking_id}/status", response_model=bool)
async def update_booking_status(
        booking_id: int,
        status: Status,
        service: BookingService = Depends(get_booking_service),
):
    return await service.update_booking_status(
        booking_id=booking_id,
        new_status=status
    )
@router.get("/bookings/{booking_id}", response_model=BookingRead)
async def get_booking_by_id(
    booking_id: int,
    service: BookingService = Depends(get_booking_service),
):
    return await service.get_booking_by_id(booking_id)
@router.get("/bookings/{booking_id}/status", response_model=str)
async def get_booking_status(
        booking_id: int,
        service: BookingService = Depends(get_booking_service),
):
    return await service.get_booking_status(booking_id)
@router.get("/bookings/user/{user_id}", response_model=list[BookingRead])
async def get_user_bookings(
        user_id: int,
        service: BookingService = Depends(get_booking_service),
):
    return await service.get_bookings_by_user_id(user_id)

@router.delete("/bookings/{booking_id}", response_model=bool)
async def delete_booking(
        booking_id: int,
        service: BookingService = Depends(get_booking_service),
) -> bool:
    booking = await service.get_booking_by_id(booking_id)
    can_delete = booking.status in [Status.CANCELLED, Status.COMPLETED]

    if not can_delete:
        raise BookingNotCompletedError
    return await service.delete_booking(booking_id)

#BOOKINGEND=================================================


#HOTEL=================================================
@router.post("/hotels", response_model=HotelRead)
async def create_hotel(
        data: HotelCreate,
        service: HotelService = Depends(get_hotel_service),
):
    return await service.add_hotel(
        data=data
    )
@router.patch("/hotels/{hotel_id}/edit", response_model=HotelRead)
async def edit_hotel(
        hotel_id: int,
        data: HotelEdit,
        service: HotelService = Depends(get_hotel_service),
):
    return await service.edit_hotel(
        hotel_id=hotel_id,
        data=data
    )
@router.get("/hotels/{hotel_id}", response_model=HotelRead)
async def get_hotel_by_id(
        hotel_id: int,
        service: HotelService = Depends(get_hotel_service),
):
    return await service.get_hotel_by_id(hotel_id)
@router.delete("/hotels/{hotel_id}", status_code=204)
async def delete_hotel(
        hotel_id: int,
        service: HotelService = Depends(get_hotel_service),
):
    return await service.delete_hotel(hotel_id)
#HOTELEND=================================================


#TOKEN
@router.post("/token/clean-up", response_model=int)
async def token_clean_up(
        service: TokenService = Depends(get_token_service),
):
    return await service.clean_up_expired_tokens()
#TOKENEND