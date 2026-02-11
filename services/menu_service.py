from models.hotel import Hotel


def menu_main():
        print('''
1) Chose Hotel
2) See my bookings
3) Exit
        ''')

def print_sorted_hotel(hotels_sorted_stars:dict[int,Hotel]):
    print("\nHotel List:")
    print(f"{'ID': <3}{'NAME': <19}{'CITY': <15}{'STARS': <10}")
    for hotel in hotels_sorted_stars.values():
        print(f"{hotel.hotel_id: <3}{hotel.name: <19}{hotel.city: <15}{hotel.stars: <10}")
