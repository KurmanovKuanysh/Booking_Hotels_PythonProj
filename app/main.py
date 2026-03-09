from app.db.session import SessionLocal
from app.services.hotel import HotelService
from app.db.init_db import init_db

from app.services.room import RoomService
from app.services.booking import BookingService
from app.services.user import UserService
from app.services.hotel import HotelService
from app.services.room_type import RoomTypeService
from app.utils.views.printers import Printer
from app.services.additional.input_service import Inputs
from app.utils.views.menus import Menu

from app.app import App

room = RoomService(SessionLocal())
booking = BookingService(SessionLocal())
user = UserService(SessionLocal())
hotel = HotelService(SessionLocal())
room_type = RoomTypeService(SessionLocal())

printers = Printer(hotel, room, booking, user)
input_service = Inputs()
menus = Menu()

app = App(
    inp=input_service,
    pr=printers,
    hotel=hotel,
    room=room,
    booking=booking,
    user=user,
    menus=menus,
    room_type=room_type
)

def main():
    app.login_menu_flow()

if __name__ == "__main__":
    main()