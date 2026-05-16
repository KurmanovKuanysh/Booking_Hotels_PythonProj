from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_db, get_current_user
from sqlalchemy.orm import Session

from backend.app.schemas.booking import BookingRead, BookingEdit, BookingCreate, BookingCancelResponse
from backend.app.schemas.user import UserRead
from backend.app.services.booking import BookingService

router = APIRouter(tags=["Bookings"])

async def get_booking_service(
        db: AsyncSession = Depends(get_db)
):
    return BookingService(db)

@router.post("/bookings", response_model=BookingRead, status_code=201)
async def create_booking(
    booking: BookingCreate,
    user: UserRead = Depends(get_current_user),
    service: BookingService = Depends(get_booking_service),
):
    return await service.create_new_booking(
        user_id=user.id,
        data=booking
    )

@router.get("/bookings/me", response_model=list[BookingRead])
async def get_user_bookings(
        user: UserRead = Depends(get_current_user),
        service: BookingService = Depends(get_booking_service),
):
    return await service.get_bookings_by_user_id(user.id)

@router.patch("/bookings/{booking_id}", response_model=BookingRead)
async def edit_booking_user(
        booking_id: int,
        data: BookingEdit,
        service: BookingService = Depends(get_booking_service),
        user: UserRead = Depends(get_current_user)
):
    return await service.edit_booking_user_side(
        user_id=user.id,
        booking_id=booking_id,
        edit=data
    )
@router.patch("/bookings/{booking_id}/cancel", response_model=BookingCancelResponse)
async def cancel_booking(
        booking_id: int,
        service: BookingService = Depends(get_booking_service),
        user: UserRead = Depends(get_current_user)
):
    return await service.cancel_booking(
        booking_id=booking_id,
        user_id=user.id,
    )