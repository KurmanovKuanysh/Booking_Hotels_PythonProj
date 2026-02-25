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
            self.pr.print_user_bookings(user_bookings, self.hotels.hotels, self.rooms.rooms)
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
            x,email = self.book_room_menu_flow(room_id, check_in, check_out, hotel_id)
            if x:
                self.payment_menu_flow(email)
            else:
                print("Canceled!")

    def payment_menu_flow(self, user_email: str):
        self.menu.print_payment_menu()
        choice = self.inp.text("Enter your choice: ")
        match choice:
            case None:
                return
            case "1":
                print("Pay by card(to do)")
                card_number = self.inp.text("Enter card number: ")
                card_cvv = self.inp.text("Enter card cvv: ",min_value=100, max_value=999)
                if self.complete_booking_menu_flow(user_email):
                    print("Booking successful!")
                    self.storage.save_bookings(self.bookings.bookings)
                    return
            case "2":
                print("Pay by Kaspi(to do_)")
                if self.complete_booking_menu_flow(user_email):
                    print("Booking successful!")
                    self.storage.save_bookings(self.bookings.bookings)
                    return
            case "3":
                print("Pay by cash(to do)")
                if self.complete_booking_menu_flow(user_email):
                    print("Booking successful!")
                    self.storage.save_bookings(self.bookings.bookings)
                    return
            case "4":
                print("Booking Details")
                self.pr.print_user_bookings([self.bookings.get_booking_by_email(user_email)], self.hotels.hotels, self.rooms.rooms)
                return
            case "5":
                print("Change the date or room(to do)")
                return
            case "0":
                print("Canceled!")
                return
            case _:
                print("Invalid choice")
    def complete_booking_menu_flow(self, email: str) -> bool:
        booking = self.bookings.get_booking_id_by_email(email)
        if self.bookings.set_booking_status(booking, "confirmed"):
            return True
        return False
    def book_room_menu_flow(self, room_id: int, check_in: date, check_out: date, hotel_id: int) -> tuple[bool, str] | bool:
        user_name = self.inp.text("Enter Your name(0 to exit):")
        if user_name is None:
            return False
        user_email = self.inp.text_email("Enter Your email(0 to exit):")
        if user_email is None:
            return False
        if not self.bookings.create_new_booking_reserve(hotel_id,room_id, user_name, check_in, check_out, user_email):
            return False
        print("Booking successful reserved!")
        self.storage.save_bookings(self.bookings.bookings)
        return True , user_email

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
                    self.admin_hotels_menu_flow()
                case "2":
                    self.admin_rooms_menu_flow()
                case "3":
                    self.pr.print_bookings(self.bookings.get_all_bookings())
                case "4":
                    self.pr.print_hotels(self.hotels.hotels)
                    while True:
                        self.menu.menu_admin_show_rooms()
                        choice = self.inp.text("Enter your choice: ")
                        match choice:
                            case None:
                                return
                            case "1":
                                h_id = self.enter_hotel_id()
                                print(f"Rooms in hotel {h_id}:")
                                self.pr.print_rooms(self.rooms.get_by_hotel_id(h_id))
                            case "2":
                                self.pr.print_rooms(self.rooms.rooms)
                            case _:
                                print("Invalid choice")
                                continue
    def enter_hotel_id(self) -> int | None:
        while True:
            hotel_id = self.inp.text_int("Enter hotel id(0 to back) ", min_value=0)
            if hotel_id == 0:
                print("Canceled!")
                break
            if not self.hotels.get_by_id(hotel_id):
                print("Hotel not found!")
                continue
            return hotel_id
    def admin_hotels_menu_flow(self):
        while True:
            self.menu.menu_admin_panel_hotels()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    if self.admin_hotel_add_menu_flow():
                        print("Hotel added successfully!")
                    else:
                        print("Hotel not added!")
                case "2":
                    self.admin_rooms_menu_flow()
                case "3":
                    self.delete_hotel_flow()
                case "4":
                    self.pr.print_hotels(self.hotels.hotels)
                case _:
                    print("Invalid choice")
    def delete_hotel_flow(self):
        h_id = self.inp.text_int("Enter hotel id to delete(0 to back): ", min_value=0)
        if h_id is None:
            return
        if self.hotels.delete_hotel(h_id):
            print("Hotel deleted successfully!")
        else:
            print("Hotel not found!")

    def admin_hotel_edit_menu_flow(self):
        print("Enter hotel id to edit:(0 to back): ")
        h_id = self.inp.text_int("Enter your hotel ID: ")
        if h_id is None:
            return
        while True:
            if self.hotels.get_by_id(h_id) is None:
                print("Hotel not found!")
                break
            self.pr.print_hotel(self.hotels.get_by_id(h_id))
            self.menu.menu_hotels_edit()
            choice = self.inp.text("Enter your choice: ")
            new_name = None
            new_city = None
            new_stars = None
            match choice:
                case None:
                    return
                case "1":
                    new_stars = self.inp.text_float("Enter new stars(0 to back): ")
                    if new_stars is None:
                        return
                case "2":
                    new_name = self.inp.text("Enter new name(0 to back): ").strip().capitalize()
                    if new_name is None:
                        return
                case "3":
                    new_city = self.inp.text("Enter new city(0 to back): ").strip().capitalize()
                    if new_city is None:
                        return
                case _:
                    print("Invalid choice")
                    continue
            if new_name is None and new_city is None and new_stars is None:
                print("No changes made!")
            self.adm.edit_exist_hotel(self.hotels.hotels , h_id, new_name, new_city, new_stars)
            break


    def admin_hotel_add_menu_flow(self) -> bool:
        hotel_name = self.inp.text("Enter hotel name(0 to back): ").title()
        if hotel_name is None:
            return False
        hotel_address = self.inp.text("Enter hotel address(0 to back`: ").strip()
        if hotel_address is None:
            return False
        hotel_city = self.inp.text("Enter hotel city(0 to back): ").title()
        if hotel_city is None:
            return False
        hotel_stars = self.inp.text_float("Enter hotel stars(0 to back): ", min_value=1, max_value=5)
        if hotel_stars is None:
            return False
        new_hotel = Hotel(
            hotel_id = max(self.hotels.hotels.keys()) + 1 if self.hotels.hotels else 1,
            city = hotel_city,
            name = hotel_name,
            address= hotel_address,
            stars = float(hotel_stars)
        )
        if self.hotels.add_hotel(new_hotel):
            return True
        return False

    def admin_rooms_menu_flow(self):
        while True:
            self.menu.menu_admin_panel_rooms()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None | "0":
                    return
                case "1":
                    h_id = self.inp.text_int("Enter hotel id to edit rooms(0 to back): ", min_value=0)
                    if h_id is None:
                        continue
                    self.pr.print_rooms(self.rooms.get_by_hotel_id(h_id))
                case "2":
                    self.pr.print_rooms(self.rooms.rooms)
                case "3":
                    self.admin_room_edit_flow()
                case "4":
                    self.add_room_flow()
                case "5":
                    self.delete_room_flow()
                case _:
                    print("Invalid choice")

    def add_room_flow(self):
        r_id = max(self.rooms.rooms.keys()) + 1 if self.rooms.rooms else 1
        hotel_id = self.inp.text_int("Enter hotel id(0 to back): ", min_value=0)
        if hotel_id is None:
            return
        number = self.inp.text_int("Enter room number(0 to back): ", min_value=0)
        if number is None:
            return
        for v in self.rooms.rooms.values():
            if v.hotel_id == hotel_id and str(v.number) == number:
                print("Room already exists in this hotel!")
                return
        room_type = self.inp.text("Enter room type(0 to back): ").strip().upper()
        if room_type is None:
            return
        capacity = self.inp.text_int("Enter room capacity(0 to back): ", min_value=0)
        if capacity is None:
            return
        room_price = self.inp.text_int("Enter room price(0 to back: ", min_value=0)
        if room_price is None:
            return
        floor = self.inp.text_int("Enter room floor(0 to back: ", min_value=0)
        if floor is None:
            return
        new_room = Room(
            r_id = r_id,
            hotel_id = hotel_id,
            number = number,
            type = RoomType(room_type),
            capacity = capacity,
            price_for_day = room_price,
            floor = floor
        )
        self.rooms.add_room(new_room)
        self.storage.save_rooms(self.rooms.rooms)
        print("Room added successfully!")

    def edit_room_flow(self):
        room_id = self.inp.text_int("Enter room id to edit(0 to back): ", min_value=0)
        if room_id is None:
            return
        room = self.rooms.rooms.get_by_id(room_id)
        if not room:
            print("Room not found!")
            return
        while True:
            self.menu.menu_rooms_edit()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None | "0":
                    return
                case "1":
                    new_hotel_id = self.inp.text_int("Enter new hotel id(0 to back): ", min_value=0)
                    if new_hotel_id is None:
                        continue
                    if self.hotels.get_by_id(new_hotel_id) is None:
                        print("Hotel not found!")
                        continue
                    self.rooms.update_room(room, hotel_id=new_hotel_id)
                case "2":
                    new_number = self.inp.text_int("Enter new room number(0 to back): ", min_value=0)
                    if new_number is None:
                        continue
                    for k,v in self.rooms.rooms.items():
                        if v.number == new_number and k != room_id:
                            print("Room already exists!")
                            continue
                    self.rooms.update_room(room, number=new_number)
                case "3":
                    new_type = self.inp.text("Enter new room type(0 to back): ").strip().upper()
                    if new_type is None:
                        continue
                    try:
                        self.rooms.update_room(room, type=RoomType(new_type))
                    except ValueError:
                        print("Invalid room type!")
                        continue
                case "4":
                    new_capacity = self.inp.text_int("Enter new room capacity(0 to back): ", min_value=0)
                    if new_capacity is None:
                        continue
                    self.rooms.update_room(room, capacity=new_capacity)
                case "5":
                    new_price = self.inp.text_int("Enter new room price(0 to back: ", min_value=0)
                    if new_price is None:
                        continue
                    self.rooms.update_room(room, price_for_day=new_price)
                case "6":
                    new_floor = self.inp.text_int("Enter new room floor(0 to back: ", min_value=0)
                    if new_floor is None:
                        continue
                    self.rooms.update_room(room, floor=new_floor)
                case _:
                    print("Invalid choice")


    def delete_room_flow(self):
        delete_id = self.inp.text_int("Enter room id to delete(0 to back): ", min_value=0)
        if delete_id is None:
            return
        self.rooms.delete_room(delete_id)
        self.storage.save_rooms(self.rooms.rooms)
        print("Room deleted successfully!")

    def admin_room_edit_flow(self):
        self.pr.print_rooms(self.rooms.rooms)
        room_id = self.inp.text_int("Enter room id to edit(0 to back): ", min_value=0)
        if room_id is None:
            return
        room = self.rooms.get_by_id(room_id)
        if not room:
            print("Room not found!")
            return
        while True:
            print(f"Editing room {room_id}")
            print('''
            1) Price
            2) Capacity
            3) Room Type
            4) Hotel ID
            0) Save and Back
            ''')
            choice = self.inp.text("Choose option: ")
            match choice:
                case None | "0":
                    self.storage.save_rooms(self.rooms.rooms)
                    print("Saving...")
                    return
                case "1":
                    new_price = self.inp.text_int("New price: ", min_value=1)
                    if new_price is None:
                        continue
                    room.price_for_day = new_price
                case "2":
                    new_capacity = self.inp.text_int("New capacity: ", min_value=1)
                    if new_capacity is None:
                        continue
                    room.capacity = new_capacity
                case "3":
                    self.pr.print_room_types(self.rooms_types)
                    rt = self.inp.text("Enter room type: ")
                    if rt is None:
                        continue
                    try:
                        room.type = RoomType(rt.upper())
                    except ValueError:
                        print("Invalid room type!")
                case "4":
                    new_hotel_id = self.inp.text_int("New hotel id: ", min_value=1)
                    if new_hotel_id is None:
                        continue
                    if not self.hotels.get_by_id(new_hotel_id):
                        print("Hotel not found!")
                        continue
                    room.hotel_id = new_hotel_id

                case _:
                    print("Invalid choice")