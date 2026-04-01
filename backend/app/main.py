from fastapi import FastAPI
from backend.app.api.routers.hotel import router as hotel_router
from backend.app.api.routers.room import router as room_router
from backend.app.api.routers.admin import router as admin_router
from backend.app.api.routers.booking import router as booking_router
from backend.app.api.routers.user import router as user_router
from backend.app.api.routers.auth import router as auth_router

from backend.app.core.exceptions_handler import (
    register_errors_handlers,login_errors_handlers,
    user_errors_handlers, booking_errors_handlers
)

app = FastAPI()
register_errors_handlers(app)
login_errors_handlers(app)
user_errors_handlers(app)
booking_errors_handlers(app)
@app.get("/")
def home():
    return {"message": "Welcome to Hotel Booking API"}

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(room_router)
app.include_router(hotel_router)
app.include_router(booking_router)
app.include_router(admin_router)