from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.booking import Status
from backend.app.core.exceptions import (
    InvalidLoginOrPasswordError,
    UserNotFoundError,
    DuplicateEmailError,
    InvalidPasswordError, BookingNotCompletedError,
)

from backend.app.models import Booking
from backend.app.models.user import User, UserRole
from backend.app.schemas.user import UserRead
from backend.app.core.security import hash_password, verify_password


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, name: str, email: str, password: str, role: UserRole):
        user = User(
            name=name,
            email=email,
            password=password,
            role=role
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        active_booking = self.session.scalar(
            select(Booking)
            .where(Booking.user_id == user_id, Booking.status.in_([Status.CONFIRMED, Status.PENDING]))
        )
        if active_booking is not None:
            raise BookingNotCompletedError
        await self.session.delete(user)
        await self.session.commit()
        return True


    async def find_user_by_email(self, email: str) -> User | None:
        return await self.session.scalar(
            select(User).where(User.email == str(email).strip().lower())
        )

    async def get_user_by_email(self, email: str) -> User | None:
        user = await self.find_user_by_email(email)
        if user is None:
            raise UserNotFoundError
        return user

    async def exists_user_email(self, email: str, exclude_uid: int | None = None) -> bool:
        user =  await self.find_user_by_email(email)
        if user is None:
            return False
        if exclude_uid is not None and user.id == exclude_uid:
            return False
        return True

    async def get_user_by_id(self, user_id: int):
        user = await self.session.scalar(
            select(User)
            .where(User.id == user_id))
        if not user:
            raise UserNotFoundError
        return user

    async def get_users_by_name(self, name: str) -> list[User]:
        users = (await self.session.scalars(select(User).where(User.name.ilike(f"%{name.strip()}%")))).all()
        if not users:
            raise UserNotFoundError
        return list(users)

    async def get_users(self) -> list[UserRead]:
        all_users = (await self.session.scalars(select(User))).all()
        return list(all_users)

    async def register_user(
            self,
            name: str,
            email: str,
            password: str,
            role = UserRole.USER
    ) -> User:
        new_password = hash_password(password)
        return await self.add_user(name, email, new_password ,role)

    async def login_user(self, email: str, password: str) -> User:
        user = await self.get_user_by_email(email)
        if not user or not verify_password(password, user.password):
            raise InvalidLoginOrPasswordError
        return user

    async def edit_user(
            self,
            uid: int,
            edit,
            commit: bool = True
    ) -> User:
        user = await self.get_user_by_id(uid)
        if edit.name is not None:
            user.name = edit.name.strip().title()

        if edit.email is not None:
            new_email = edit.email.strip().lower()
            if await self.exists_user_email(edit.email, exclude_uid=uid):
                raise DuplicateEmailError
            user.email = new_email

        if edit.password is not None:
            if " " in edit.password:
                raise InvalidPasswordError
            user.password = hash_password(edit.password)

        if commit:
            await self.session.commit()
            await self.session.refresh(user)
        return user

    async def edit_user_admin(
            self,
            uid: int,
            edit
    ) -> User:
        user = await self.edit_user(
            uid=uid,
            edit=edit,
            commit=False
        )
        if edit.is_active is not None:
            if edit.is_active in [True, False]:
                user.is_active = edit.is_active
        if edit.role is not None and edit.role in [UserRole.ADMIN, UserRole.USER, UserRole.S_ADMIN]:
            user.role = edit.role

        await self.session.commit()
        await self.session.refresh(user)
        return user