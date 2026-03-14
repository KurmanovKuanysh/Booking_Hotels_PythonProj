from backend.app.models.room import Room

class App:
    def __init__(self, menus, inp, pr, hotel, room, booking, user, room_type, admin):
        self.menus = menus
        self.inp = inp
        self.pr = pr
        self.hotel = hotel
        self.room = room
        self.booking = booking
        self.user = user
        self.room_type = room_type
        self.admin = admin

        self.current_user = None

        self.hotel_filters = {
            "city": None,
            "stars_from": 1,
            "stars_to": 5,
        }

        self.room_filters = {
            "hotel_id": None,
            "price_from": None,
            "price_to": None,
            "capacity": None,
            "room_type": None,
        }

    def login_menu_flow(self):
        while True:
            self.menus.login_menu()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    self.login_user()
                case "2":
                    self.register_menu_flow()
                case "4":
                    self.current_user = self.user.get_user_by_email("kukatop01@gmail.com")
                    self.main_menu_flow()
                case _:
                    print("Invalid choice")
                    continue
    def login_user(self):
        while True:
            email = self.inp.text_email("Enter your email(0 to back): ")
            if email is None:
                return
            user = self.user.get_user_by_email(email)
            if user is None:
                print("User not found, try again or register new account!")
                continue
            password = self.inp.text_password("Enter your password(0 to back): ")
            if password is None:
                return
            if self.user.check_password(user.id, password):
                self.current_user = user
                print("Login successful!")
                self.main_menu_flow()
                return
            else:
                print("Invalid password")
                continue

    def register_menu_flow(self):
        while True:
            email = self.inp.text_email("Enter your email(0 to back): ")
            if email is None:
                return
            if self.user.get_user_by_email(email):
                print("Email already exists")
                continue
            password = self.inp.text_password("Enter your password(0 to back): ")
            if password is None:
                return
            name = self.inp.text("Enter your name(0 to back): ")
            if name is None:
                return

            self.user.register_user(
                name=name.strip().capitalize(),
                password=password,
                email=email,
                role="USER"
            )
            self.current_user = self.user.get_user_by_email(email)
            print("Registration successful!")
            self.main_menu_flow()
            return


    def main_menu_flow(self):
        while True:
            self.menus.menu_main()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    self.find_hotel_menu_flow()
                case "2":
                    self.user_bookings_menu_flow()
                case "3":
                    if self.current_user and self.current_user.role == "ADMIN":
                        self.admin_panel_menu_flow()
                        return
                    else:
                        print("Access denied!")
                case _:
                    print("Invalid choice")
                    continue
    def admin_panel_menu_flow(self):
        while True:
            self.menus.menu_admin_panel()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    self.admin_hotel_flow()
                case "2":
                    self.admin_room_flow()
                case "3":
                    self.admin_booking_flow()
                case "4":
                    self.admin_user_flow()
    def admin_hotel_flow(self):
        pass

    def admin_room_flow(self):
        pass
    def admin_user_flow(self):
        pass

    def admin_booking_flow(self):
        pass
    def user_bookings_menu_flow(self):
        if self.current_user is None:
            print("You are not logged in!")
            return

        user_bookings = self.booking.get_bookings_by_user_id(self.current_user.id)
        if not user_bookings:
            print("No bookings found")
            return
        self.pr.print_user_bookings(user_bookings)

    def find_hotel_menu_flow(self):
        while True:
            self.menus.menu_find_hotel()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    self.search_hotel_by_name_flow()
                case "2":
                    self.filters_menu_flow()
                case _:
                    print("Invalid choice")
                    continue

    def filters_menu_flow(self):
        while True:
            if self.hotel_filters:
                self.pr.print_hotel_filters(self.hotel_filters)
            self.menus.menu_filters()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    city = self.inp.text("Enter city(0 to back): ")
                    if city is None:
                        continue
                    self.hotel_filters["city"] = city
                case "2":
                    self.set_stars_flow()
                case "3":
                    hotels = self.hotel.list_hotels_by_filter(self.hotel_filters)
                    if not hotels:
                        print("No hotels found")
                        continue
                    self.pr.print_hotels(hotels)
                    self.booking_choice_menu_flow()
                case _:
                    print("Invalid choice")
                    continue

    def set_stars_flow(self):
        while True:
            stars_from = self.inp.text_float("Enter stars from(0 to back: ", min_value=0, max_value=5)
            if stars_from == 0:
                continue
            stars_to = self.inp.text_float("Enter stars to(0 to back): ", min_value=0, max_value=5)
            if stars_to == 0:
                continue
            if stars_from > stars_to:
                self.hotel_filters["stars_from"], self.hotel_filters["stars_to"] = stars_to, stars_from
            else:
                self.hotel_filters["stars_from"], self.hotel_filters["stars_to"] = stars_from, stars_to
            print(f"Saved Stars: {stars_from} - {stars_to}")
            break

    def search_hotel_by_name_flow(self):
        while True:
            name = self.inp.text("Enter hotel name(0 to back): ")
            if name is None:
                print("\nCanceled!")
                break
            hotels = self.hotel.get_hotel_by_name(name.strip().lower())
            if not hotels:
                print("\nNo hotels found")
                break
            self.pr.print_hotels(hotels)
            self.booking_choice_menu_flow()
            return

    def booking_choice_menu_flow(self):
        while True:
            hotel_id = self.inp.text_int("Enter hotel id to book(0 to back):", min_value=0)
            if hotel_id == 0:
                return
            hotel = self.hotel.get_hotel_by_id(hotel_id)
            if not hotel:
                print("Hotel not found, try again or change Filters!")
                continue
            print(f"Chosen Hotel: {hotel.name}\n")
            rooms = self.room.list_rooms_by_hotel_id(hotel_id)
            self.from_hotel_to_room_flow(rooms, hotel_id)
            return


    def from_hotel_to_room_flow(self, rooms: list[Room], hotel_id: int):
        while True:
            self.menus.menu_choose_room_filter()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    break
                case "1":
                    print("\nOpening filters...\n")
                    self.room_filters_menu_flow(rooms, hotel_id)
                    continue
                case "2":
                    print("\nAll rooms:\n")
                    self.pr.print_rooms(rooms)
                    continue
                case "3":
                    print("\nChoose room:\n")
                    self.choose_room_flow(rooms, hotel_id)
                    return
                case _:
                    print("Invalid choice")
                    continue

    def room_filters_menu_flow(self, rooms: list[Room], hotel_id: int):
        while True:
            if self.room_filters:
                self.pr.print_room_filters(self.room_filters)
            self.menus.room_filters_menu()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    break
                case "1":
                    ranges = self.room.get_price_range(rooms)
                    print(f"Price range: {ranges['min']}$ - {ranges['max']}$")
                    print("\nEnter new ranges!")
                    min_price = self.inp.text_float("Enter minimal price: ", min_value=ranges['min'])
                    max_price = self.inp.text_float("Enter maximal price: ", max_value=ranges['max'])
                    if min_price > max_price:
                        min_price, max_price = max_price, min_price
                    self.room_filters["price_from"] = min_price
                    self.room_filters["price_to"] = max_price
                    print(f"Saved price range {min_price}-{max_price}!\n")
                    continue

                case "2":
                    room_types = self.room_type.get_types(rooms)
                    self.pr.print_room_types(self.room_type.get_types(rooms))

                    room_type = self.inp.text("Enter room type(0 to exit): ")
                    if room_type is None:
                        break

                    room_type_name = room_type.strip().lower()

                    if room_type_name not in [rt.type_name.lower() for rt in room_types]:
                        print("Invalid room type")
                        continue

                    self.room_filters["room_type"] = room_type_name
                    print(f"Saved room type {room_type_name}!\n")
                    continue
                case "3":
                    max_capacity = max(rooms, key=lambda x: x.capacity).capacity
                    print(f"\n\nMax capacity: {max_capacity}\n")
                    person = self.inp.text_int("Enter room capacity(0 to exit): ", min_value=0, max_value=max_capacity)
                    if person == 0:
                        break
                    self.room_filters["capacity"] = person
                    print(f"Saved capacity {person}!\n")
                    continue

                case "4":
                    print("\nFiltered rooms:\n")
                    rooms_filtered = self.room.get_rooms_by_filter(hotel_id, self.room_filters)
                    self.pr.print_rooms(rooms_filtered)
                    continue
                case "5":
                    rooms_filtered = self.room.get_rooms_by_filter(hotel_id, self.room_filters)
                    if not rooms_filtered:
                        print("No rooms found, try again or change Filters!")
                        continue
                    self.choose_room_flow(rooms_filtered, hotel_id)
                case "6":
                    self.room_filters = {
                        "hotel_id": None,
                        "price_from": None,
                        "price_to": None,
                        "capacity": None,
                        "room_type": None,
                    }
                    print("Filters cleared!")
                    continue
                case _:
                    print("Invalid choice")
                    continue

    def choose_room_flow(self, rooms: list[Room], hotel_id: int):
        while True:
            print("Chosen Hotel")
            self.pr.print_hotel(self.hotel.get_hotel_by_id(hotel_id))
            print("\nRooms:")
            self.pr.print_rooms(rooms)
            room_id = self.inp.text_int("Enter room id(0 to exit): ", min_value=0)
            if room_id == 0:
                break
            room = self.room.get_room_by_id(room_id)
            if not room:
                print("Room not found, try again!")
                continue
            print(f"\nChosen Room {room_id}\n")
            self.pr.print_room(room)
            self.choose_date_flow(room_id)
            return
    def choose_date_flow(self, room_id: int):
        while True:
            print("Enter check in/out date!")
            dates = self.inp.text_date_range()
            if dates is None:
                print("Canceled!")
                break
            check_in, check_out = dates
            if not self.room.is_room_available(room_id, check_in, check_out):
                print("Room is not available for that date range!")
                continue
            print("Room is available!")
            new_booking = self.booking.create_new_booking(
                r_id=room_id,
                check_in=check_in,
                check_out=check_out,
                status="pending",
                user_id=self.current_user.id
            )
            if new_booking is not None:
                print("Booking reserved!")
                self.payment_menu_flow()
                return
            else:
                print("Booking failed!")
                continue

    def payment_menu_flow(self):
        while True:
            self.menus.print_payment_menu()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    print("Pay by card(to do)")
                    card_number = self.inp.text("Enter card number: ")
                    if card_number is None:
                        print("Canceled!")
                        return
                    card_cvv = self.inp.text_int("Enter card cvv: ", min_value=100, max_value=999)

                    last_booked = self.booking.get_last_booking_of_user(self.current_user.id)
                    if last_booked:
                        self.booking.confirm_booking(last_booked.id)
                        print("Booking successful!")
                        return

                case "2":
                    print("Pay by Kaspi(to do)")
                    last_booked = self.booking.get_last_booking_of_user(self.current_user.id)
                    if last_booked:
                        self.booking.confirm_booking(last_booked.id)
                        print("Booking successful!")
                        return
                case "3":
                    print("Pay by cash(to do)")
                    last_booked = self.booking.get_last_booking_of_user(self.current_user.id)
                    if last_booked:
                        self.booking.confirm_booking(last_booked.id)
                        print("Booking successful!")
                        return
                case "4":
                    print("Booking Details")
                    booking = self.booking.get_last_booking_of_user(self.current_user.id)
                    if not booking:
                        print("No bookings found")
                        return
                    self.pr.print_user_bookings(list(booking))
                    return
                case "5":
                    print("Change the date or room(to do)")
                    return
                case "0":
                    print("Canceled!")
                case _:
                    print("Invalid choice")
                    continue