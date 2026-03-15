
import pytest

from backend.app.models.user import User

from backend.app.services.user import UserService
from sqlalchemy.orm import Session
from sqlalchemy import select

@pytest.fixture
def user_admin(session: Session):
    service = UserService(session)
    user = service.add_user(
        name="Kuka",
        email="kuka@kuka.com",
        password="password",
        role="ADMIN"
    )
    return user

@pytest.fixture
def user_one(session: Session):
    service = UserService(session)
    user = service.add_user(
        name="Test User",
        email="testuser@gmail.com",
        password="password",
        role="USER"
    )
    return user

def test_add_user(session: Session):
    service = UserService(session)

    users = session.scalars(select(User)).all()
    assert users == []

    user = service.add_user(
        name="Test User",
        email="testuser@gmail.com",
        password="password",
        role="USER"
    )

    result = session.scalars(
        select(User)
        .where(User.id == user.id)
    ).one_or_none()

    assert result == user

def test_add_user_duplicate_email(session: Session, user_one: User):
    service = UserService(session)

    with pytest.raises(ValueError, match="User with this email already exists"):
        service.add_user(
            name="Test User2",
            email="testuser@gmail.com",
            password="password",
            role="USER"
        )

def test_get_user_by_email(session:Session, user_one: User):
    service = UserService(session)

    user_by_email = service.get_user_by_email(user_one.email)
    assert user_by_email == user_one

def test_get_user_by_email_not_found(session:Session):
    service = UserService(session)

    with pytest.raises(ValueError, match="User not found"):
        service.get_user_by_email("nonexistent@gmail.com")

def test_delete_user_return_true(session: Session, user_one: User):
    service = UserService(session)

    user = service.get_user_by_id(user_one.id)
    assert user == user_one

    deleted = service.delete_user(user_one.id)
    assert deleted is True

def test_delete_user_return_false(session: Session, user_one: User):
    service = UserService(session)

    deleted = service.delete_user(-1)
    assert deleted is False

    user = service.get_user_by_id(user_one.id)
    assert user == user_one

    delete_user = service.delete_user(user_one.id)
    assert delete_user is True

def test_edit_user_return_user(session: Session, user_one: User):
    service = UserService(session)

    user = service.get_user_by_id(user_one.id)
    assert user.name == user_one.name

    edit: dict = {
        "id": user_one.id,
        "name": "New Name",
        "email": "newmail@mail.ru",
        "password": "newpassword",
        "role": "USER"
    }

    edited_user = service.edit_user(edit)
    assert edited_user.name == "New Name"
    assert edited_user.email == "newmail@mail.ru"
    assert edited_user.password == "newpassword"
    assert edited_user.role == "USER"

