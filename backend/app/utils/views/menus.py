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
=====Setting Filters=====

    1) City
    2) Stars
    3) Show hotels by this filter
    0) Back
    
=====Setting Filters=====
    """)

    def menu_choose_room_filter(self):
        print("""
    1) Room Filters
    2) Show all rooms
    3) Choose room
    0) Back
        """)

    def room_filters_menu(self):
        print("""
    1) Price
    2) Room type
    3) Room capacity
    4) Show all rooms
    5) Continue Booking
    6) Reset Filters
    0) Back
    """)

    def menu_bookings(self):
        print('''
    1) Book hotel
    0) Back
    ''')

    def menu_admin_panel(self):
        print('''
    1) Hotels Control
    2) Rooms Control
    3) Bookings Control
    4) User Control
    0) Back
        ''')

    def menu_admin_panel_hotels(self):
        print('''
    1) Add hotel
    2) Edit existing hotel
    3) Delete hotel
    4) Show all hotels
    0) Back
        ''')

    def print_payment_menu(self):
        print(r'''
    ╔══════════════════════════════════════════════════════════════╗
    ║                    💳 ОПЛАТА БРОНИ ОТЕЛЯ                     ║
    ╠══════════════════════════════════════════════════════════════╣
    ║ Выберите способ оплаты:                                      ║
    ║                                                              ║
    ║  1) 💳 Банковская карта (Visa / MasterCard)                  ║
    ║  2) 🏦 Kaspi Pay / QR                                         ║
    ║  3) 💸 Наличными при заселении                               ║
    ║  4) 🧾 Безналичный счет (для организаций)                    ║
    ║                                                              ║
    ╠══════════════════════════════════════════════════════════════╣
    ║ Дополнительно:                                               ║
    ║  5) 📄 Посмотреть детали брони                               ║
    ║  6) 🔁 Изменить даты / номер                                 ║
    ║  0) 🔙 Назад(Отменить бронирование)                                                 ║
    ╠══════════════════════════════════════════════════════════════╣
    ║ Примечание:                                                  ║
    ║ • Условия отмены и возврата зависят от тарифа.               ║
    ║ • Возможна комиссия банка/платежной системы.                 ║
    ╚══════════════════════════════════════════════════════════════╝

    Введите номер пункта и нажмите Enter: 
    ''')

    def menu_admin_panel_rooms(self):
        print("""
    ==================== ROOMS ADMIN =====================

      1) Show rooms by hotel
      2) Show all rooms
      3) Edit room
      4) Add room
      5) Delete room
      0) Back

    ======================================================
    """)
    def menu_admin_show_rooms(self):
        print('''
    1) Show rooms by hotel id
    2) Show all rooms
    0) Back
        ''')

    def menu_hotels_edit(self):
        print('''
    1) Edit star
    2) Edit city
    3) Edit address
    4) Edit name
    0) Back
        ''')
    def menu_rooms_edit(self):
        print('''
    1) Edit room's hotel id
    2) Edit room's number
    3) Edit room's type
    4) Edit room's capacity
    5) Edit room's price
    6) Edit room's floor
    0) Save and Back
        ''')

    def login_menu(self):
        print('''
        1) Login
        2) Register
        4) Login Fast
        0) Exit
        ''')

    def menu_admin_panel_users(self):
        print('''
    1) Show users
    2) Add user
    3) Edit user
    4) Delete user
    0) Back
        ''')

    def menu_admin_users_edit(self):
        print('''
    1) Edit user's name
    2) Edit user's email
    3) Edit user's password
    4) Edit user's role
    0) Back
        ''')

    def menu_admin_panel_bookings(self):
        print('''
    1) Show bookings
    2) Add booking
    3) Edit booking
    4) Delete booking
    0) Back
        ''')

    def menu_admin_bookings_edit(self):
        print('''
    1) Edit Booking Status
    2) Edit Booking Date
    3) Edit Booking Room
    0) Back
        ''')