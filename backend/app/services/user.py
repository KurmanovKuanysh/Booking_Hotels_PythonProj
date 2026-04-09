from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.exceptions import (
    InvalidLoginOrPasswordError,
    UserNotFoundError,
    DuplicateEmailError,
    InvalidPasswordError,
)

from backend.app.models import Booking
from backend.app.models.user import User
from fastapi import HTTPException

from backend.app.schemas.user import UserRead

from backend.app.core.security import hash_password, verify_password

class UserService:
    def __init__(self, session: Session):
        self.session = session

    def add_user(self, name: str, email: str, password: str, role: str):
        user = User(
            name=name,
            email=email,
            password=password,
            role=role
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            active_booking = self.session.scalar(
                select(Booking)
                .where(Booking.user_id == user_id, Booking.status.in_(["confirmed", "pending"]))
            )
            if active_booking is not None:
                raise HTTPException(status_code=400, detail="User has active bookings!")
            self.session.delete(user)
            self.session.commit()
            return True
        raise HTTPException(status_code=404, detail="User not found")

    def find_user_by_email(self, email: str) -> User | None:
        return self.session.scalars(
            select(User).where(User.email == str(email).strip().lower())
        ).one_or_none()

    def get_user_by_email(self, email: str) -> User | None:
        user = self.find_user_by_email(email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def exists_user_email(self, email: str, exclude_uid: int | None = None) -> bool:
        user = self.find_user_by_email(email)
        if user is None:
            return False
        if exclude_uid is not None and user.id == exclude_uid:
            return False
        return True

    def get_user_by_id(self, user_id: int):
        user = self.session.scalars(
            select(User)
            .where(User.id == user_id)).first()
        if not user:
            raise UserNotFoundError
        return user

    def get_users_by_name(self, name: str) -> list[User]:
        users = self.session.scalars(select(User).where(User.name.ilike(f"%{name.strip()}%"))).all()
        if not users:
            raise HTTPException(status_code=404, detail="User not found")
        return list(users)

    def get_users(self) -> list[UserRead]:
        all_users = self.session.scalars(select(User)).all()
        return list(all_users)

    def register_user(
            self,
            name: str,
            email: str,
            password: str,
            role = "USER"
    ) -> User:
        new_password = hash_password(password)
        return self.add_user(name, email, new_password ,role)

    def login_user(self, email: str, password: str) -> User:
        user = self.get_user_by_email(email)
        if not user or not verify_password(password, user.password):
            raise InvalidLoginOrPasswordError
        return user

    def edit_user(
            self,
            uid: int,
            edit,
            commit: bool = True
    ) -> User:
        user = self.get_user_by_id(uid)
        if edit.name is not None:
            user.name = edit.name.strip().title()

        if edit.email is not None:
            new_email = edit.email.strip().lower()
            if self.exists_user_email(edit.email, exclude_uid=uid):
                raise DuplicateEmailError(email=edit.email)
            user.email = new_email

        if edit.password is not None:
            if " " in edit.password:
                raise InvalidPasswordError
            user.password = hash_password(edit.password)

        if commit:
            self.session.commit()
            self.session.refresh(user)
        return user

    def edit_user_admin(
            self,
            uid: int,
            edit
    ) -> User:
        user = self.edit_user(
            uid=uid,
            edit=edit,
            commit=False
        )
        if edit.is_active is not None:
            if edit.is_active in [True, False]:
                user.is_active = edit.is_active
        if edit.role is not None and edit.role in ["USER", "ADMIN", "S-ADMIN"]:
            user.role = edit.role

        self.session.commit()
        self.session.refresh(user)
        return user
    def get_user_bookings(self, user) -> list[Booking]:
        return list(self.session.scalars(
            select(Booking)
            .where(Booking.user_id == user.id,
                   Booking.status.in_(["confirmed"]))
        ))