from fastapi import APIRouter, Depends, HTTPException
from backend.app.api.deps import get_db
from backend.app.schemas.user import  UserCreate, UserRead, UserLogin, UserRegister
from backend.app.services.user import UserService
from sqlalchemy.orm import Session
from backend.app.core.security import verify_password, create_access_token
from datetime import timedelta
from fastapi.responses import JSONResponse

REFRESH_TOKEN_EXPIRE_DAYS = 2
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserRead)
def create_user(
        user: UserCreate,
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
@router.post("/register", response_model=UserRead, status_code=201)
def create_user_account(
        user_data: UserRegister,
        db: Session = Depends(get_db)
):
    service = UserService(db)

    if service.get_user_by_email(user_data.email) is not None:
        raise HTTPException(status_code=400, detail="User with this Email already registered")

    new_user = service.register_user(
        user_data.name,
        user_data.email,
        user_data.password
    )
    return new_user
@router.post("/login")
def login_user(
        user_data: UserLogin,
        db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.get_user_by_email(user_data.email)

    if user is not None:
        password_valid = verify_password(user_data.password, user.password)
        if password_valid:
            access_token = create_access_token(
                data={
                    'email':user.email,
                }
            )
            refresh_token = create_access_token(
                data={
                    'email':user.email,
                },
                refresh=True,
                expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user" : {
                        "email":user.email
                    }
                }
            )
    raise HTTPException(status_code=403, detail="Invalid email or password")

@router.get("/{user_id}", response_model=UserRead)
def get_user_by_id(user_id:int , db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_user_by_id(user_id)
@router.delete("/{user_id}", response_model=bool)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.delete_user(user_id)