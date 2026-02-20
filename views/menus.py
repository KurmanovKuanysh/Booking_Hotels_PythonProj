class Menu:
    def menu_main(self):
        print("""
    1) Find hotel
    2) My bookings
    3) Admin panel
    0) Exit
    """)

    def menu_find_hotel(self):
        print("""
    1) Search by name
    2) Hotel Filters
    0) Back
    """)

    def menu_filters(self):
        print("""
    1) City
    2) Stars
    3) Show hotels by this filter
    0) Back
    """)

    def menu_choose_room_filter(self):
        print("""
    1) Room Filters
    2) Show all rooms
    3) Continue Booking
    0) Back
        """)

    def room_filters_menu(self):
        print("""
    1) Price
    2) Room type
    3) Room capacity
    4) Show all rooms
    5) Continue Booking
    0) Back
    """)

    def menu_bookings(self):
        print('''
    1) Book hotel
    0) Back
    ''')

    def menu_admin_panel(self):
        print('''
    1) Hotels Edit
    2) Rooms Edit
    3) Show all bookings
        ''')

    def menu_hotels_edit(self):
        print('''
    1) Add hotel
    2) Edit existing hotel
    3) Delete hotel
    0) Exit
        ''')
    def menu_rooms_edit(self):
        print('''
    1) Add room
    2) Edit existing room
    3) Delete room
    0) Exit
        ''')