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
                case _:
                    print("Invalid choice")
                    continue
    def admin_hotel_flow(self):
        while True:
            self.menus.menu_admin_panel_hotels()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    self.admin_add_hotel_flow()
                case "2":
                    self.admin_edit_hotel_choice_flow()
                case "3":
                    self.admin_delete_hotel_flow()
                case "4":
                    hotels = self.admin.get_hotels()
                    if not hotels:
                        print("No hotels found!")
                        continue
                    self.pr.print_hotels(hotels)
                case _:
                    print("Invalid choice")
                    continue

    def admin_edit_hotel_choice_flow(self):
        hotels = self.admin.get_hotels()
        if not hotels:
            print("No hotels found!")
            return
        self.pr.print_hotels(hotels)
        hotel_id = self.inp.text_int("Enter hotel id to edit(0 to back): ", min_value=0)
        if hotel_id == 0:
            return
        hotel = self.hotel.get_hotel_by_id(hotel_id)
        if not hotel:
            print("Hotel not found!")
            return
        print(f"\nEditing hotel: {hotel.name}")
        self.admin_edit_hotel_flow(hotel_id)

    def admin_edit_hotel_flow(self, hotel_id: int):
        while True:
            self.menus.menu_hotels_edit()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    stars = self.inp.text_float("Enter new stars 1-5(0 to back): ", min_value=0, max_value=5)
                    if stars == 0:
                        continue
                    self.admin.edit_hotel({"id": hotel_id, "stars": stars})
                    print("Stars updated!")
                case "2":
                    city = self.inp.text("Enter new city(0 to back): ")
                    if city is None:
                        continue
                    self.admin.edit_hotel({"id": hotel_id, "city": city.strip().capitalize()})
                    print("City updated!")
                case "3":
                    address = self.inp.text("Enter new address(0 to back): ")
                    if address is None:
                        continue
                    self.admin.edit_hotel({"id": hotel_id, "address": address.strip()})
                    print("Address updated!")
                case "4":
                    name = self.inp.text("Enter new name(0 to back): ")
                    if name is None:
                        continue
                    self.admin.edit_hotel({"id": hotel_id, "name": name.strip().capitalize()})
                    print("Name updated!")
                case _:
                    print("Invalid choice")
                    continue

    def admin_delete_hotel_flow(self):
        hotels = self.admin.get_hotels()
        if not hotels:
            print("No hotels found!")
            return
        self.pr.print_hotels(hotels)
        hotel_id = self.inp.text_int("Enter hotel id to delete(0 to back): ", min_value=0)
        if hotel_id == 0:
            return
        hotel = self.hotel.get_hotel_by_id(hotel_id)
        if not hotel:
            print("Hotel not found!")
            return
        confirm = self.inp.text(f"Delete hotel '{hotel.name}'? (yes/0 to cancel): ")
        if confirm is None or confirm.lower() != "yes":
            print("Canceled!")
            return
        try:
            result = self.admin.delete_hotel(hotel_id)
            if result:
                print("Hotel deleted successfully!")
            else:
                print("Failed to delete hotel!")
        except ValueError as e:
            print(f"Error: {e}")

    def admin_add_hotel_flow(self):
        name = self.inp.text("Enter hotel name(0 to back): ")
        if name is None:
            return
        city = self.inp.text("Enter city(0 to back): ")
        if city is None:
            return
        stars = self.inp.text_float("Enter stars 1-5(0 to back): ", min_value=0, max_value=5)
        if stars == 0:
            return
        address = self.inp.text("Enter address(0 to back): ")
        if address is None:
            return
        hotel = self.admin.add_new_hotel(
            hotel_name=name.strip().capitalize(),
            hotel_city=city.strip().capitalize(),
            hotel_stars=stars,
            hotel_address=address.strip()
        )
        if hotel:
            print(f"\nHotel '{hotel.name}' added successfully! ID: {hotel.id}")
        else:
            print("Failed to add hotel!")

    def admin_room_flow(self):
        while True:
            self.menus.menu_admin_panel_rooms()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    hotel_id = self.inp.text_int("Enter hotel id(0 to back): ", min_value=0)
                    if hotel_id == 0:
                        continue
                    rooms = self.room.list_rooms_by_hotel_id(hotel_id)
                    if not rooms:
                        print("No rooms found for this hotel!")
                        continue
                    self.pr.print_rooms(rooms)
                case "2":
                    rooms = self.admin.get_rooms()
                    if not rooms:
                        print("No rooms found!")
                        continue
                    self.pr.print_rooms(rooms)
                case "3":
                    self.admin_edit_room_choice_flow()
                case "4":
                    self.admin_add_room_flow()
                case "5":
                    self.admin_delete_room_flow()
                case _:
                    print("Invalid choice")
                    continue

    def admin_add_room_flow(self):
        hotels = self.admin.get_hotels()
        if not hotels:
            print("No hotels found!")
            return
        self.pr.print_hotels(hotels)
        hotel_id = self.inp.text_int("Enter hotel id(0 to back): ", min_value=0)
        if hotel_id == 0:
            return
        hotel = self.hotel.get_hotel_by_id(hotel_id)
        if not hotel:
            print("Hotel not found!")
            return

        room_number = self.inp.text("Enter room number(0 to back): ")
        if room_number is None:
            return

        all_room_types = self.room_type.get_all_types()
        self.pr.print_room_types(all_room_types)
        room_type_id = self.inp.text_int("Enter room type id(0 to back): ", min_value=0)
        if room_type_id == 0:
            return
        if not any(rt.id == room_type_id for rt in all_room_types):
            print("Invalid room type id!")
            return

        capacity = self.inp.text_int("Enter capacity(0 to back): ", min_value=0)
        if capacity == 0:
            return
        price = self.inp.text_float("Enter price per day(0 to back): ", min_value=0)
        if price == 0:
            return
        floor = self.inp.text_int("Enter floor(0 to back): ", min_value=0)
        if floor == 0:
            return
        description = self.inp.text("Enter description(Enter to skip, 0 to back): ")

        room = self.admin.add_new_room(
            hotel_id=hotel_id,
            room_number=room_number.strip(),
            room_type_id=room_type_id,
            capacity=capacity,
            price_per_day=price,
            floor=floor,
            description=description
        )
        if room:
            print(f"\nRoom #{room.id} added to hotel '{hotel.name}' successfully!")
        else:
            print("Failed to add room!")

    def admin_edit_room_choice_flow(self):
        rooms = self.admin.get_rooms()
        if not rooms:
            print("No rooms found!")
            return
        self.pr.print_rooms(rooms)
        room_id = self.inp.text_int("Enter room id to edit(0 to back): ", min_value=0)
        if room_id == 0:
            return
        room = self.room.get_room_by_id(room_id)
        if not room:
            print("Room not found!")
            return
        print(f"\nEditing room #{room_id} (hotel: {room.h_id})")
        self.admin_edit_room_flow(room_id)

    def admin_edit_room_flow(self, room_id: int):
        while True:
            self.menus.menu_rooms_edit()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    hotels = self.admin.get_hotels()
                    self.pr.print_hotels(hotels)
                    new_hotel_id = self.inp.text_int("Enter new hotel id(0 to back): ", min_value=0)
                    if new_hotel_id == 0:
                        continue
                    if not self.hotel.get_hotel_by_id(new_hotel_id):
                        print("Hotel not found!")
                        continue
                    self.admin.edit_room({"id": room_id, "h_id": new_hotel_id})
                    print("Hotel updated!")
                case "2":
                    room_number = self.inp.text("Enter new room number(0 to back): ")
                    if room_number is None:
                        continue
                    self.admin.edit_room({"id": room_id, "room_number": room_number.strip()})
                    print("Room number updated!")
                case "3":
                    all_room_types = self.room_type.get_all_types()
                    self.pr.print_room_types(all_room_types)
                    room_type_id = self.inp.text_int("Enter new room type id(0 to back): ", min_value=0)
                    if room_type_id == 0:
                        continue
                    if not any(rt.id == room_type_id for rt in all_room_types):
                        print("Invalid room type id!")
                        continue
                    self.admin.edit_room({"id": room_id, "r_t_id": room_type_id})
                    print("Room type updated!")
                case "4":
                    capacity = self.inp.text_int("Enter new capacity(0 to back): ", min_value=0)
                    if capacity == 0:
                        continue
                    self.admin.edit_room({"id": room_id, "capacity": capacity})
                    print("Capacity updated!")
                case "5":
                    price = self.inp.text_float("Enter new price per day(0 to back): ", min_value=0)
                    if price == 0:
                        continue
                    self.admin.edit_room({"id": room_id, "price_per_day": price})
                    print("Price updated!")
                case "6":
                    floor = self.inp.text_int("Enter new floor(0 to back): ", min_value=0)
                    if floor == 0:
                        continue
                    self.admin.edit_room({"id": room_id, "floor": floor})
                    print("Floor updated!")
                case _:
                    print("Invalid choice")
                    continue

    def admin_delete_room_flow(self):
        rooms = self.admin.get_rooms()
        if not rooms:
            print("No rooms found!")
            return
        self.pr.print_rooms(rooms)
        room_id = self.inp.text_int("Enter room id to delete(0 to back): ", min_value=0)
        if room_id == 0:
            return
        room = self.room.get_room_by_id(room_id)
        if not room:
            print("Room not found!")
            return
        confirm = self.inp.text(f"Delete room #{room_id}? (yes/0 to cancel): ")
        if confirm is None or confirm.lower() != "yes":
            print("Canceled!")
            return
        try:
            result = self.admin.delete_room(room_id)
            if result:
                print("Room deleted successfully!")
            else:
                print("Failed to delete room!")
        except ValueError as e:
            print(f"Error: {e}")

    def admin_user_flow(self):
        while True:
            self.menus.menu_admin_panel_users()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    users = self.admin.get_users()
                    if not users:
                        print("No users found!")
                        continue
                    self.pr.print_users(users)
                case "2":
                    self.admin_add_user_flow()
                case "3":
                    self.admin_edit_user_choice_flow()
                case "4":
                    self.admin_delete_user_flow()
                case _:
                    print("Invalid choice")
                    continue

    def admin_add_user_flow(self):
        name = self.inp.text("Enter name(0 to back): ")
        if name is None:
            return
        email = self.inp.text_email("Enter email(0 to back): ")
        if email is None:
            return
        if self.user.exists_user_email(email):
            print("Email already exists!")
            return
        password = self.inp.text_password("Enter password(0 to back): ")
        if password is None:
            return
        print("Roles: USER / ADMIN")
        role = self.inp.text("Enter role(0 to back): ")
        if role is None:
            return
        if role.upper() not in ("USER", "ADMIN"):
            print("Invalid role!")
            return
        new_user = self.admin.admin_add_user(
            name=name.strip().capitalize(),
            email=email,
            password=password,
            role=role.upper()
        )
        if new_user:
            print(f"\nUser '{new_user.name}' added successfully! ID: {new_user.id}")
        else:
            print("Failed to add user!")

    def admin_edit_user_choice_flow(self):
        users = self.admin.get_users()
        if not users:
            print("No users found!")
            return
        self.pr.print_users(users)
        user_id = self.inp.text_int("Enter user id to edit(0 to back): ", min_value=0)
        if user_id == 0:
            return
        user = self.user.get_user_by_id(user_id)
        if not user:
            print("User not found!")
            return
        print(f"\nEditing user: {user.name} ({user.email})")
        self.admin_edit_user_flow(user_id)

    def admin_edit_user_flow(self, user_id: int):
        while True:
            self.menus.menu_admin_users_edit()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    name = self.inp.text("Enter new name(0 to back): ")
                    if name is None:
                        continue
                    self.admin.edit_user({"id": user_id, "name": name.strip().capitalize()})
                    print("Name updated!")
                case "2":
                    email = self.inp.text_email("Enter new email(0 to back): ")
                    if email is None:
                        continue
                    if self.user.get_user_by_email(email):
                        print("Email already in use!")
                        continue
                    self.admin.edit_user({"id": user_id, "email": email})
                    print("Email updated!")
                case "3":
                    password = self.inp.text_password("Enter new password(0 to back): ")
                    if password is None:
                        continue
                    self.admin.edit_user({"id": user_id, "password": password})
                    print("Password updated!")
                case "4":
                    print("Roles: USER / ADMIN")
                    role = self.inp.text("Enter new role(0 to back): ")
                    if role is None:
                        continue
                    if role.upper() not in ("USER", "ADMIN"):
                        print("Invalid role!")
                        continue
                    self.admin.edit_user({"id": user_id, "role": role.upper()})
                    print("Role updated!")
                case _:
                    print("Invalid choice")
                    continue

    def admin_delete_user_flow(self):
        users = self.admin.get_users()
        if not users:
            print("No users found!")
            return
        self.pr.print_users(users)
        user_id = self.inp.text_int("Enter user id to delete(0 to back): ", min_value=0)
        if user_id == 0:
            return
        user = self.user.get_user_by_id(user_id)
        if not user:
            print("User not found!")
            return
        if user_id == self.current_user.id:
            print("You cannot delete yourself!")
            return
        confirm = self.inp.text(f"Delete user '{user.name}'? (yes/0 to cancel): ")
        if confirm is None or confirm.lower() != "yes":
            print("Canceled!")
            return
        try:
            result = self.admin.delete_user(user_id)
            if result:
                print("User deleted successfully!")
            else:
                print("Failed to delete user!")
        except ValueError as e:
            print(f"Error: {e}")

    def admin_booking_flow(self):
        while True:
            self.menus.menu_admin_panel_bookings()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    bookings = self.admin.get_bookings()
                    if not bookings:
                        print("No bookings found!")
                        continue
                    self.pr.print_user_bookings(bookings)
                case "2":
                    self.admin_add_booking_flow()
                case "3":
                    self.admin_edit_booking_choice_flow()
                case "4":
                    self.admin_delete_booking_flow()
                case _:
                    print("Invalid choice")
                    continue

    def admin_add_booking_flow(self):
        users = self.admin.get_users()
        if not users:
            print("No users found!")
            return
        self.pr.print_users(users)
        user_id = self.inp.text_int("Enter user id(0 to back): ", min_value=0)
        if user_id == 0:
            return
        user = self.user.get_user_by_id(user_id)
        if not user:
            print("User not found!")
            return

        rooms = self.admin.get_rooms()
        if not rooms:
            print("No rooms found!")
            return
        self.pr.print_rooms(rooms)
        room_id = self.inp.text_int("Enter room id(0 to back): ", min_value=0)
        if room_id == 0:
            return
        room = self.room.get_room_by_id(room_id)
        if not room:
            print("Room not found!")
            return

        print("Enter booking dates:")
        dates = self.inp.text_date_range()
        if dates is None:
            print("Canceled!")
            return
        check_in, check_out = dates

        if not self.room.is_room_available(room_id, check_in, check_out):
            print("Room is not available for this date range!")
            return

        print("Statuses: pending / confirmed / cancelled")
        status = self.inp.text("Enter status(0 to back): ")
        if status is None:
            return
        if status.lower() not in ("pending", "confirmed", "cancelled"):
            print("Invalid status!")
            return

        booking = self.admin.add_new_booking(
            r_id=room_id,
            check_in=check_in,
            check_out=check_out,
            status=status.lower(),
            user_id=user_id
        )
        if booking:
            print(f"\nBooking #{booking.id} created successfully!")
        else:
            print("Failed to create booking!")

    def admin_edit_booking_choice_flow(self):
        bookings = self.admin.get_bookings()
        if not bookings:
            print("No bookings found!")
            return
        self.pr.print_user_bookings(bookings)
        booking_id = self.inp.text_int("Enter booking id to edit(0 to back): ", min_value=0)
        if booking_id == 0:
            return
        booking = self.booking.get_booking_by_id(booking_id)
        if not booking:
            print("Booking not found!")
            return
        print(f"\nEditing booking #{booking_id}")
        self.admin_edit_booking_flow(booking_id)

    def admin_edit_booking_flow(self, booking_id: int):
        while True:
            self.menus.menu_admin_bookings_edit()
            choice = self.inp.text("Enter your choice: ")
            match choice:
                case None:
                    return
                case "1":
                    print("Statuses: pending / confirmed / cancelled")
                    status = self.inp.text("Enter new status(0 to back): ")
                    if status is None:
                        continue
                    if status.lower() not in ("pending", "confirmed", "cancelled"):
                        print("Invalid status!")
                        continue
                    self.admin.edit_booking({"id": booking_id, "status": status.lower()})
                    print("Status updated!")
                case "2":
                    print("Enter new booking dates:")
                    dates = self.inp.text_date_range()
                    if dates is None:
                        continue
                    check_in, check_out = dates
                    self.admin.edit_booking({"id": booking_id, "check_in": check_in, "check_out": check_out})
                    print("Dates updated!")
                case "3":
                    rooms = self.admin.get_rooms()
                    if not rooms:
                        print("No rooms found!")
                        continue
                    self.pr.print_rooms(rooms)
                    room_id = self.inp.text_int("Enter new room id(0 to back): ", min_value=0)
                    if room_id == 0:
                        continue
                    if not self.room.get_room_by_id(room_id):
                        print("Room not found!")
                        continue
                    self.admin.edit_booking({"id": booking_id, "r_id": room_id})
                    print("Room updated!")
                case _:
                    print("Invalid choice")
                    continue

    def admin_delete_booking_flow(self):
        bookings = self.admin.get_bookings()
        if not bookings:
            print("No bookings found!")
            return
        self.pr.print_user_bookings(bookings)
        booking_id = self.inp.text_int("Enter booking id to delete(0 to back): ", min_value=0)
        if booking_id == 0:
            return
        booking = self.booking.get_booking_by_id(booking_id)
        if not booking:
            print("Booking not found!")
            return
        confirm = self.inp.text(f"Delete booking #{booking_id}? (yes/0 to cancel): ")
        if confirm is None or confirm.lower() != "yes":
            print("Canceled!")
            return
        try:
            result = self.admin.delete_booking(booking_id)
            if result:
                print("Booking deleted successfully!")
            else:
                print("Failed to delete booking!")
        except ValueError as e:
            print(f"Error: {e}")

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