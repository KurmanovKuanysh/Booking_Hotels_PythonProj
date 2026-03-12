from backend.app.db.session import SessionLocal

from backend.app.services.room import RoomService
from backend.app.services.booking import BookingService
from backend.app.services.user import UserService
from backend.app.services.hotel import HotelService
from backend.app.services.room_type import RoomTypeService
from backend.app.utils.views.printers import Printer
from backend.app.services.additional.input_service import Inputs
from backend.app.utils.views.menus import Menu
from backend.app.services.admin import Admin

from backend.app.app import App

session = SessionLocal()
try:
    room = RoomService(session)
    booking = BookingService(session)
    user = UserService(session)
    hotel = HotelService(session)
    room_type = RoomTypeService(session)
    admin = Admin(session)
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
    room_type=room_type,
    admin=admin
    )
finally:
    session.close()

def main():
    app.login_menu_flow()

if __name__ == "__main__":
    main()