from models.hotel import Hotel
from models.room import Room
from models.room_types import RoomType
from datetime import date


class App:
    def __init__(self,storage, booking_s, hotel_s, room_s, printers, input_service, filters, menu, room_typex, admin):
        self.storage = storage
        self.bookings = booking_s
        self.hotels = hotel_s
        self.rooms = room_s
        self.pr = printers
        self.inp = input_service
        self.filter_s = filters
        self.menu = menu
        self.rooms_types = room_typex
        self.adm = admin

    def main_menu_flow(self):
        while True:
            self.menu.menu_main()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    self.find_hotel_menu_flow()
                case "2":
                    self.user_bookings_menu_flow()
                case "3":
                    self.admin_panel_menu_flow()
                case _:
                    print("Invalid choice")
                    continue
    def user_bookings_menu_flow(self):
        while True:
            user_email = self.inp.text_email("Enter your email(0 to exit): ")
            if user_email is None:
                return
            user_bookings = self.bookings.get_user_bookings(user_email)
            if not user_bookings:
                print("No bookings found")
                break
            self.pr.print_user_bookings(user_bookings, self.hotels, self.rooms)
            break


    def find_hotel_menu_flow(self):
        while True:
            self.menu.menu_find_hotel()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    self.search_hotel_by_name_menu_flow()
                case "2":
                    self.filters_menu_flow()
                case _:
                    print("Invalid choice")
                    continue
    def filters_menu_flow(self):
        while True:
            self.menu.menu_filters()
            self.pr.print_active_filters(self.filter_s.get_active_filters())
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    break
                case "1":
                    city = self.inp.text("Enter city: ")
                    if city is None:
                        break
                    self.filter_s.set_filter_city(city)
                case "2":
                    self.stars_menu_flow()
                case "3":
                    filtered_hotels = self.filter_s.get_hotels_by_filters(self.hotels.hotels)
                    self.pr.print_hotels(filtered_hotels)
                    self.booking_choice_menu_flow(filtered_hotels)
                case _:
                    print("Invalid choice")
                    continue
    def booking_choice_menu_flow(self, hotels_new: dict[int, Hotel]):
        while True:
            print("Wanna book hotel? (y/n)")
            choice = self.inp.text_yes_no()
            if choice:
                self.booking_menu_flow(hotels_new)
            else:
                break
    def search_hotel_by_name_menu_flow(self):
        while True:
            name = self.inp.text("Enter hotel name(0 to back): ")
            if name is None:
                break
            hotels_by_name = self.hotels.find_by_name(name)
            if not hotels_by_name:
                print("No hotels found")
                break
            self.pr.print_hotels(hotels_by_name)
            self.booking_choice_menu_flow(hotels_by_name)

    def stars_menu_flow(self):
        while True:
            stars_from = self.inp.text_int("Enter stars from(0 to back): ", min_value=0, max_value=5)
            if stars_from == 0:
                break
            stars_to = self.inp.text_int("Enter stars to(0 to back): ", min_value=0, max_value=5)
            if stars_to == 0:
                break

            if stars_from > stars_to:
                stars_from, stars_to = stars_to, stars_from

            self.filter_s.set_filter_stars(stars_from, stars_to)
            print(f"saved stars: {stars_from}-{stars_to}")
            break

    def booking_menu_flow(self,hotels_by_name: dict[int, Hotel]):
        if not hotels_by_name:
            return
        while True:
            self.pr.print_hotels(hotels_by_name)
            hotel_id = self.inp.text_int("Enter hotel id(0 to back):", min_value=0)
            if hotel_id == 0:
                break
            hotel = hotels_by_name.get(hotel_id)
            if not hotel:
                print("Hotel not found, try again or chance Filters!")
                continue
            rooms_new = self.rooms.get_by_hotel_id(hotel_id)
            print(f"Chosen Hotel: {hotel.name}\n")
            self.from_hotel_to_room_menu_flow(rooms_new, hotel_id)

    def from_hotel_to_room_menu_flow(self, rooms_new: dict[int, Room], hotel_id: int):
        while True:
            self.menu.menu_choose_room_filter()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    break
                case "1":
                    print("\nOpening filters...\n")
                    self.room_filters_menu_flow(rooms_new, hotel_id)
                case "2":
                    self.pr.print_rooms(rooms_new)
                case "3":
                    self.choose_room_menu_flow(rooms_new, hotel_id)
                case _:
                    print("Invalid choice")
                    continue

    def choose_room_menu_flow(self, rooms_new: dict[int, Room], hotel_id: int):
        while True:
            print("Chosen Hotel")
            self.pr.print_hotel(self.hotels.get_by_id(hotel_id))
            print("\nRooms:")
            self.pr.print_rooms(rooms_new)
            room_id = self.inp.text_int("Enter room id(0 to exit): ", min_value=0)
            if room_id == 0:
                break
            if not rooms_new.get(room_id):
                print("Room not found, try again!")
                continue
            print(f"\nChosen Room {room_id}\n")
            self.date_range_menu_flow(room_id, hotel_id)


    def date_range_menu_flow(self, room_id: int, hotel_id: int):
        while True:
            print("Enter check in/out date!")
            dates = self.inp.text_date_range()
            if dates is None:
                print("Canceled!")
                break
            check_in, check_out = dates
            if not self.rooms.is_available_rooms(room_id, self.bookings.bookings, check_in, check_out):
                print("Room is not available for that date range!")
                continue
            print("Room is available!")
            if self.book_room_menu_flow(room_id, check_in, check_out, hotel_id):
                print("Main menu")
                self.main_menu_flow()
            else:
                print("Canceled!")


    def book_room_menu_flow(self, room_id: int, check_in: date, check_out: date, hotel_id: int) -> bool:
        user_name = self.inp.text("Enter Your name(0 to exit):")
        if user_name is None:
            return False
        user_email = self.inp.text_email("Enter Your email(0 to exit):")
        if user_email is None:
            return False
        if not self.bookings.create_new_booking_reserve(hotel_id,room_id, user_name, check_in, check_out, user_email):
            return False
        print("Booking successful!")
        self.storage.save_bookings(self.bookings.bookings)
        return True

    def room_filters_menu_flow(self, rooms_new: dict[int, Room], hotel_id: int):
        while True:
            self.menu.room_filters_menu()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    break
                case "1":
                    ranges = self.rooms.get_price_range(rooms_new)
                    print(f"Price range: {ranges['min_price']}$ - {ranges['max_price']}$")
                    minimal_price = self.inp.text_int("Enter minimal price: ", min_value=ranges['min_price'])
                    maximal_price = self.inp.text_int("Enter maximal price: ", max_value=ranges['max_price'])
                    if minimal_price > maximal_price:
                        minimal_price, maximal_price = maximal_price, minimal_price
                    self.filter_s.set_filter_price_range(minimal_price, maximal_price)
                    print("Saved price range!\n")
                case "2":
                    self.pr.print_room_types(self.rooms_types)
                    room_type = self.inp.text("Enter room type: ").strip()
                    if room_type is None:
                        break
                    try:
                        rt = RoomType(room_type.upper())
                    except ValueError:
                        print("Invalid room type")
                        continue
                    if self.filter_s.set_filter_room_type(rt):
                        print("Saved room type!\n")
                    else:
                        print("Invalid room type")
                case "3":
                    max_capacity = max(rooms_new.values(), key=lambda x: x.capacity).capacity
                    print(f"Max capacity: {max_capacity}\n")
                    self.filter_s.set_filter_capacity(self.inp.text_int("Enter room capacity: ", min_value=1, max_value=max_capacity))
                    print("Saved capacity!\n")
                case "4":
                    print("\nFiltered rooms:\n")
                    self.pr.print_rooms(self.filter_s.get_rooms_by_filter(rooms_new))
                case "5":
                    self.choose_room_menu_flow(rooms_new, hotel_id)
                case _:
                    print("Invalid choice")
    def admin_panel_menu_flow(self):
        while True:
            self.menu.menu_admin_panel()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    self.menu.menu_hotels_edit()
                case "2":
                    self.menu.menu_rooms_edit()
                case "3":
                    self.pr.print_bookings(self.bookings.bookings.get_all_bookings())