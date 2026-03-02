from datetime import date
from app.services.booking_service import create_booking, list_user_bookings
from app.services.hotel_service import get_hotel_by_id, find_hotels_by_name
from app.services.hotel_service import list_hotels
from app.services.room_service import list_rooms_by_hotel_id

# def main():
#     hotel = get_hotel_by_id(1)
#     print(f"Hotel: {hotel['name']}")
#
#     name = "main"
#     new_hotels = find_hotels_by_name(name)
#     if new_hotels:
#         print(f"Found hotels: {new_hotels}")
def main():
    hotels = list_hotels()
    print("HOTELS:", hotels)

    if hotels:
        h_id = hotels[0]["id"]
        print("ROOMS FOR HOTEL", h_id)
        for r in list_rooms_by_hotel_id(h_id):
            print(r)
if __name__ == "__main__":
    main()