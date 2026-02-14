from dataclasses import dataclass
from datetime import date

@dataclass
class Booking:
    booking_id:int
    hotel_id:int
    r_id:int
    name_client:str
    checkin_date:date
    checkout_date:date
    total_price:float
    status: str

