from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_db, get_current_user
from backend.app.schemas.review import ReviewRead, ReviewCreate, ReviewEdit
from backend.app.schemas.user import UserRead
from backend.app.services.review import ReviewService

router = APIRouter(tags=["Reviews"])

async def get_review_service(
        db: AsyncSession = Depends(get_db)
):
    return ReviewService(db)

@router.get("/users/reviews", response_model=list[ReviewRead])
async def get_user_reviews(
        user: UserRead = Depends(get_current_user),
        service: ReviewService = Depends(get_review_service),
):
    return await service.get_user_reviews(user)

@router.get("/hotels/{hotel_id}/reviews", response_model=list[ReviewRead])
async def get_hotel_review(
        hotel_id: int,
        service: ReviewService = Depends(get_review_service),
):
    return await service.get_reviews(hotel_id=hotel_id)

@router.post("/hotels/{hotel_id}/reviews", response_model=ReviewRead)
async def add_hotel_review(
        hotel_id: int,
        data: ReviewCreate,
        service: ReviewService = Depends(get_review_service),
        user: UserRead = Depends(get_current_user),
):
    return await service.add_review(
        user=user,
        data=data,
        hotel_id=hotel_id,
    )

@router.patch("/reviews/{review_id}", response_model=ReviewRead)
async def edit_review(
        review_id: int,
        data: ReviewEdit,
        service: ReviewService = Depends(get_review_service),
        user: UserRead = Depends(get_current_user),
):
    return await service.edit_review(
        review_id=review_id,
        user=user,
        data=data,
    )
@router.delete("/reviews/{review_id}", status_code=204)
async def delete_review(
        review_id: int,
        service: ReviewService = Depends(get_review_service),
        user: UserRead = Depends(get_current_user),
):
    return await service.delete_review(review_id, user)