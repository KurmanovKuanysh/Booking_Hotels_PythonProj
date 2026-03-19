from fastapi import FastAPI
from backend.app.api.routers.hotel import router as hotel_router
from backend.app.api.routers.room import router as room_router
from backend.app.api.routers.user import router as user_router
from backend.app.api.routers.booking import router as booking_router
app = FastAPI()
@app.get("/")
def home():
    return {"message": "Welcome to Hotel Booking API"}

app.include_router(room_router)
app.include_router(hotel_router)
app.include_router(user_router)
app.include_router(booking_router)