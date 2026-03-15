from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.models.user import User

class UserService:
    def __init__(self, session: Session):
        self.session = session

    def add_user(self, name: str, email: str, password: str, role: str):
        if self.find_user_by_email(email):
            raise ValueError("User with this email already exists")
        user = User(name=name, email=email, password=password, role=role)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def find_user_by_email(self, email: str):
        return self.session.scalars(
            select(User).where(User.email == email)
        ).one_or_none()

    def get_user_by_email(self, email: str) -> User:
        email_user = self.find_user_by_email(email)
        if not email_user:
            raise ValueError("User not found")
        return email_user

    def exists_user_email(self, email: str) -> bool:
        return self.find_user_by_email(email) is not None

    def get_user_by_id(self, user_id: int) -> User:
        id_user = self.session.scalars(select(User).where(User.id == user_id)).first()
        return id_user

    def get_users_by_name(self, name: str) -> list[User]:
        name_user = self.session.scalars(select(User).where(User.name == name)).all()
        return list(name_user)

    def get_users(self) -> list[User]:
        all_users = self.session.scalars(select(User)).all()
        return list(all_users)

    def register_user(self, name: str, email: str, password: str, role = "USER"):
        return self.add_user(name, email, password ,role)

    def check_password(self,user_id: int, password: str) -> bool:
        user = self.get_user_by_id(user_id)
        return user.password == password

    def edit_user(self, edit: dict) -> User:
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