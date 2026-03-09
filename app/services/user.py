from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User

class UserService:
    def __init__(self, session: Session):
        self.session = session

    def add_user(self, name: str, email: str, password: str, role: str):
        if self.get_user_by_email(email):
            raise ValueError("User with this email already exists")
        user = User(name=name, email=email, password=password, role=role)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user


    def get_user_by_email(self, email: str) -> User:
        email_user = self.session.scalars(select(User).where(User.email == email)).first()
        return email_user

    def get_user_by_id(self, user_id: int) -> User:
        id_user = self.session.scalars(select(User).where(User.id == user_id)).first()
        return id_user

    def get_users_by_name(self, name: str) -> list[User]:
        name_user = self.session.scalars(select(User).where(User.name == name)).all()
        return list(name_user)

    def list_users(self) -> list[User]:
        all_users = self.session.scalars(select(User)).all()
        return list(all_users)

    def remove_user(self, user_id: int) -> bool:
        return True if self.session.delete(self.get_user_by_id(user_id))  else False

    def register_user(self, name: str, email: str, password: str, role = "USER"):
        return self.add_user(name, email, password ,role)

    def check_password(self,user_id: int, password: str) -> bool:
        user = self.get_user_by_id(user_id)
        return user.password == password