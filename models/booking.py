from dataclasses import dataclass
from datetime import date, datetime

@dataclass
class Booking:
    booking_id:int
    hotel_id:int
    r_id:int
    guest_name:str
    guest_email:str
    name_client:str
    checkin_date:date
    checkout_date:date
    total_price:float
    status: str
    created_at:datetime

