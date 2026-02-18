from services.hotel_service import HotelService
from storage import Storage
from services.booking_service import BookingService
from services.rooms_service import RoomsService
from services.filter_service import FilterService
from views.printers import Printers
from services.input_service import Inputs
from models.filter import Filter
from views.menus import Menu
from app import App

def main():
    storage = Storage()

    rooms_service = RoomsService(storage)
    hotels_service = HotelService(storage)
    bookings_service = BookingService(storage, rooms_service)

    filter_service = FilterService(Filter())
    printers = Printers()
    inputs = Inputs()
    menu = Menu()

    app = App(
            booking_s=bookings_service,
            hotel_s=hotels_service,
            room_s=rooms_service,
            printers=printers,
            input_service=inputs,
            filters=filter_service,
            menu=menu
        )
    app.main_menu_flow()


if __name__ == "__main__":
    main()
