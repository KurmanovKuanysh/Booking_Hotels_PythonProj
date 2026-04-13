from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db, get_current_user
from backend.app.schemas.review import ReviewRead, ReviewCreate, ReviewEdit
from backend.app.schemas.user import UserRead
from backend.app.services.review import ReviewService

router = APIRouter(tags=["Reviews"])

@router.get("/users/reviews", response_model=list[ReviewRead])
def get_user_reviews(
        user: UserRead = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    service = ReviewService(db)
    return service.get_user_reviews(user)
@router.post("/hotels/{hotel_id}/reviews", response_model=ReviewRead)
def add_hotel_review(
        hotel_id: int,
        data: ReviewCreate,
        db: Session = Depends(get_db),
        user: UserRead = Depends(get_current_user),
):
    service = ReviewService(db)
    return service.add_review(
        user=user,
        data=data,
        hotel_id=hotel_id,
    )
@router.patch("/reviews/{review_id}", response_model=ReviewRead)
def edit_review(
        review_id: int,
        data: ReviewEdit,
        db: Session = Depends(get_db),
        user: UserRead = Depends(get_current_user),
):
    service = ReviewService(db)
    return service.edit_review(
        review_id=review_id,
        user=user,
        data=data,
    )
@router.delete("/reviews/{review_id}", status_code=204)
def delete_review(
        review_id: int,
        db: Session = Depends(get_db),
        user: UserRead = Depends(get_current_user),
):
    service = ReviewService(db)
    return service.delete_review(review_id, user)