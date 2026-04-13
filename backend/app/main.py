from fastapi import FastAPI
from backend.app.api.routers.hotel import router as hotel_router
from backend.app.api.routers.room import router as room_router
from backend.app.api.routers.admin import router as admin_router
from backend.app.api.routers.booking import router as booking_router
from backend.app.api.routers.user import router as user_router
from backend.app.api.routers.auth import router as auth_router
from backend.app.api.routers.review import router as review_router
from backend.app.core.exceptions_handler import (
    register_errors_handlers,login_errors_handlers,
    user_errors_handlers, booking_errors_handlers,
    hotel_errors_handlers, room_errors_handlers,
    independent_errors_handlers
)
from backend.app.core.middleware import register_middleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_errors_handlers(app)
login_errors_handlers(app)
user_errors_handlers(app)
booking_errors_handlers(app)
hotel_errors_handlers(app)
room_errors_handlers(app)
independent_errors_handlers(app)

register_middleware(app)


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(room_router)
app.include_router(hotel_router)
app.include_router(booking_router)
app.include_router(admin_router)
app.include_router(review_router)

@app.get("/")
async def main():
    return {"message": "Hello World"}