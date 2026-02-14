from services.hotel_service import HotelService
from storage import Storage
from services.booking_service import BookingService
from services.rooms_service import RoomsService
from views.menu_service import print_sorted_hotel
from services.filter_service import get_active_filters
from models.filter import Filter
from services.input_service import *
from views.printers import show_active_filters
from models.room import RoomType
from services.room_types_service import choose_room_type
from views.menus import menu_main, menu_find_hotel, menu_filters

storage = Storage()

rooms_service = RoomsService(storage)
rooms = storage.load_rooms()
room_types = RoomType()
hotels_service = HotelService(storage)
bookings_service = BookingService(storage, rooms_service)
filters = Filter()

while True:
    menu_main()
    choice = text("Enter your choice: ")
    if choice == "0":
        break
    if choice == "1":
        while True:
            menu_find_hotel()
            choice_f = text("Enter your choice: ")
            if choice_f == "0":
                print("Back to main menu")
                break
            if choice_f == "1":
                s_city = text("Enter city name: ")
                hotel_city = hotels_service.find_by_city(s_city)
                if not hotel_city:
                    print("No hotels found")
                    continue
                print_sorted_hotel(hotel_city)
                hotel_id = text_int("Enter hotel ID (0 to back): ", min_value=0)
                if hotel_id == 0:
                    continue
                hotel = hotels_service.get_by_id(hotel_id)
                if not hotel:
                    print("Hotel not found")
                    continue
                print(f"Booking details for hotel {hotel.name}........")
            if choice_f == "2":
                menu_filters()
                show_active_filters(get_active_filters(filters))
                # print('''
                # 1)Stars
                # 2)Capacity
                # 3)Date in/out
                # 4)Room Type
                # 5)Show hotels by this filter
                # 0)exit filter
                #     ''')
                choice_f2 = text("Enter your choice: ")
                if choice_f2 == "0":
                    print("Back to main menu")
                    break
                if choice_f2 == "1":
                    min_stars = text_int("Enter minimum stars:", min_value=1, max_value=5)
                    max_stars = text_int("Enter maximum stars:", min_value=1, max_value=5)
                    if min_stars > max_stars:
                        min_stars,max_stars = max_stars, min_stars
                    filters.stars_to = max_stars
                    filters.stars_from = min_stars
                if choice_f2 == "2":
                    capacity = text_int("How many people can stay in the room?:", min_value=1, max_value=10)
                    filters.capacity = capacity
                if choice_f2 == "3":
                    date_in, date_out = text_date_range("Enter check-in and check-out dates (YYYY-MM-DD):")
                    if date_in and date_out:
                        filters.date_in = date_in
                        filters.date_out = date_out
                    else:
                        print("Invalid date range")
                if choice_f2 == "4":
                    r_type = choose_room_type()
                    filters.room_type = r_type





