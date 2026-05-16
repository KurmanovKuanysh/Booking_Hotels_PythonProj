from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.booking import Status
from backend.app.core.exceptions import ( InvalidNumberError, HotelNotFoundError, BookingNotFoundError, \
    ReviewNotFoundError, NoPermissionRole, DuplicateReviewError )
from backend.app.models import Booking, Hotel
from backend.app.models.filter import FReview
from backend.app.models.review import Review
from backend.app.models.user import UserRole
from backend.app.utils.utils import numeric_10_2

class ReviewService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_review(self, user, data, hotel_id: int) -> Review:  #data -> booking_id, rating, comment
        booking = await self.session.scalar(
            select(Booking)
            .where(Booking.user_id == user.id,
                   Booking.id == data.booking_id,
                   Booking.status.in_([Status.COMPLETED])
                )
        )
        if booking:
            review = await self.session.scalar(
                select(Review)
                .where(Review.booking_id == booking.id,)
            )
            if review:
                raise DuplicateReviewError
            if data.rating < 1 or data.rating > 5:
                raise InvalidNumberError
            hotel = await self.session.scalar(
                select(Hotel)
                .where(Hotel.id == hotel_id)
            )
            if hotel:
                new_review = Review(
                    user_id=user.id,
                    booking_id=booking.id,
                    hotel_id=hotel.id,
                    rating=Decimal(data.rating),
                    comment=data.comment.strip() if data.comment else None
                )
                hotel.rating_sum += new_review.rating
                hotel.rating_count += 1
                hotel.stars = numeric_10_2(hotel.rating_sum / hotel.rating_count)
                self.session.add(new_review)
                await self.session.commit()
                await self.session.refresh(new_review)

                return new_review
            raise HotelNotFoundError
        raise BookingNotFoundError

    async def get_reviews(self, hotel_id: int | None) -> list[Review]:
        query = select(Review)
        if hotel_id:
            query = query.where(Review.hotel_id == hotel_id)
        return list((await self.session.scalars(query)).all())

    async def get_review_by_id(self, review_id: int) -> Review | None:
        review = await self.session.scalar(select(Review).where(Review.id == review_id))
        if not review:
            raise ReviewNotFoundError
        return review

    async def get_user_reviews(self, user) -> list[Review]:
        return list((await self.session.scalars(select(Review).where(Review.user_id == user.id))).all())

    async def get_reviews_by_filter(self, filter_data: FReview) -> list[Review]:
        query = select(Review)
        if filter_data.hotel_id:
            if filter_data.hotel_id < 1:
                raise InvalidNumberError
            query = query.where(Review.hotel_id == filter_data.hotel_id)
        if filter_data.rating:
            if filter_data.rating < 1 or filter_data.rating > 5:
                raise InvalidNumberError
            query = query.where(Review.rating >= filter_data.rating)
        return list((await self.session.scalars(query)).all())

    async def edit_review(self, review_id: int, user, data) -> Review | None: #data -> rating, comment
        review = await self.get_review_by_id(review_id)
        if review.user_id == user.id:
            if data.rating < 1 or data.rating > 5:
                raise InvalidNumberError
            old_rating = review.rating
            review.rating = Decimal(data.rating)
            if data.comment:
                review.comment = data.comment.strip()
            hotel = await self.session.scalar(select(Hotel).where(Hotel.id == review.hotel_id))
            hotel.rating_sum = hotel.rating_sum - old_rating + data.rating
            hotel.stars = numeric_10_2(hotel.rating_sum / hotel.rating_count)

            await self.session.commit()
            return review
        raise NoPermissionRole

    async def delete_review(self, review_id: int, user) -> bool:
        review = await self.session.scalar(select(Review).where(Review.id == review_id))
        if review:
            if review.user_id != user.id and user.role != UserRole.ADMIN:
                raise NoPermissionRole
            hotel = await self.session.scalar(select(Hotel).where(Hotel.id == review.hotel_id))
            hotel.rating_sum -= review.rating
            hotel.rating_count -= 1
            hotel.stars = numeric_10_2(hotel.rating_sum / hotel.rating_count)
            await self.session.delete(review)
            await self.session.commit()
            return True
        return False
