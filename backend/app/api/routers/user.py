from fastapi import APIRouter, Depends
from backend.app.api.deps import get_db
from backend.app.schemas.user import  UserBase, UserRead, UserLogin, UserRegister
from backend.app.services.user import UserService
from sqlalchemy.orm import Session
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserRead)
def create_user(
        user: UserBase,
        db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.add_user(
        user.name,
        user.email,
        user.password,
        user.role
    )
@router.get("/email", response_model=UserRead)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_user_by_email(email)
@router.get("/name", response_model=list[UserRead])
def get_user_by_name(name: str, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_users_by_name(name)
@router.get("/", response_model=list[UserRead])
def get_all_users(db: Session = Depends(get_db) ):
    service = UserService(db)
    return service.get_users()
@router.post("/register", response_model=UserRead)
def register_user(
        user: UserRegister,
        db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.register_user(
        name=user.name,
        email=user.email,
        password=user.password
    )
@router.post("/login", response_model=UserRead)
def login_user(
        user: UserLogin,
        db: Session = Depends(get_db)):
    service = UserService(db)
    return service.login_user(
        email=user.email,
        password=user.password
    )
@router.get("/{user_id}", response_model=UserRead)
def get_user_by_id(user_id:int , db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_user_by_id(user_id)
@router.delete("/{user_id}", response_model=bool)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.delete_user(user_id)