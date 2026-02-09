from models.booking_status import BookingStatus
from dataclasses import dataclass

@dataclass
class Booking:
    booking_id:int
    hotel_id:int
    room_id:int
    name_client:str
    checkin_date:str
    checkout_date:str
    total_price:float
    status: str

