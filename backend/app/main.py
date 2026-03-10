from backend.app.db.session import SessionLocal

from backend.app.services.room import RoomService
from backend.app.services.booking import BookingService
from backend.app.services.user import UserService
from backend.app.services.hotel import HotelService
from backend.app.services.room_type import RoomTypeService
from backend.app.utils.views.printers import Printer
from backend.app.services.additional.input_service import Inputs
from backend.app.utils.views.menus import Menu

from backend.app.app import App

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