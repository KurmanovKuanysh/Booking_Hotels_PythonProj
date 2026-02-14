from models.hotel import Hotel

def print_sorted_hotel(hotels_sorted_stars:dict[int,Hotel]):
    print("\nHotel List:")
    print(f"{'ID': <3}{'NAME': <19}{'CITY': <15}{'STARS': <10}")
    for hotel in hotels_sorted_stars.values():
        print(f"{hotel.hotel_id: <3}{hotel.name: <19}{hotel.city: <15}{hotel.stars: <10}")

def check_empty(hotels:dict[int,Hotel]):
    return len(hotels) == 0