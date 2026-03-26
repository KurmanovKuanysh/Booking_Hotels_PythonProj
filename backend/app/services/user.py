from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.exceptions import InvalidLoginOrPasswordError

from backend.app.models import Booking
from backend.app.models.user import User
from fastapi import HTTPException

from backend.app.schemas.user import UserRead

from backend.app.core.security import hash_password, verify_password

class UserService:
    def __init__(self, session: Session):
        self.session = session

    def add_user(self, name: str, email: str, password: str, role: str):
        # if self.find_user_by_email(email):
        #     raise HTTPException(status_code=400, detail="Email already registered")
        user = User(name=name, email=email, password=password, role=role)
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
            select(User).where(User.email == email)
        ).one_or_none()

    def get_user_by_email(self, email: str) -> User | None:
        user = self.find_user_by_email(email)
        # if not user:
        #     raise HTTPException(status_code=404, detail="User not found")
        return user

    def exists_user_email(self, email: str) -> bool:
        return self.find_user_by_email(email) is not None

    def get_user_by_id(self, user_id: int) -> UserRead:
        user = self.session.scalars(
            select(User)
            .where(User.id == user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_users_by_name(self, name: str) -> list[User]:
        users = self.session.scalars(select(User).where(User.name.ilike(f"%{name.strip()}%"))).all()
        if not users:
            raise HTTPException(status_code=404, detail="User not found")
        return list(users)

    def get_users(self) -> list[UserRead]:
        all_users = self.session.scalars(select(User)).all()
        return list(all_users)

    def register_user(self, name: str, email: str, password: str, role = "USER"):
        new_password = hash_password(password)
        return self.add_user(name, email, new_password ,role)

    def login_user(self, email: str, password: str) -> User:
        user = self.get_user_by_email(email)
        if not user or not self.check_password(user.id, password):
            raise InvalidLoginOrPasswordError("Invalid email or password")
        return user

    def check_password(self,user_id: int, password: str) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return verify_password(password, user.password)

    def edit_user(self, edit: dict) -> UserRead:
        if "id" not in edit:
            raise ValueError("User id is required")
        user = self.get_user_by_id(edit["id"])
        if user is None:
            raise ValueError("User not found")
        if "name" in edit and edit["name"] is not None:
            if len(edit["name"]) < 3:
                raise ValueError("Name must be at least 3 characters long")
            if len(edit["name"]) > 100:
                raise ValueError("Name must be at most 100 characters long")
            user.name = edit["name"].strip()
        if "email" in edit and edit["email"] is not None:
            if len(edit["email"]) < 3:
                raise ValueError("Email must be at least 3 characters long")
            if len(edit["email"]) > 255:
                raise ValueError("Email must be at most 100 characters long")
            user.email = edit["email"].strip()
        if "password" in edit and edit["password"] is not None:
            if len(edit["password"]) < 6:
                raise ValueError("Password must be at least 6 characters")
            user.password = edit["password"]
        if "role" in edit and edit["role"] is not None:
            if edit["role"] not in ["ADMIN", "USER"]:
                raise ValueError("Role must be ADMIN or USER")
            user.role = edit["role"]
        self.session.commit()
        self.session.refresh(user)
        return user