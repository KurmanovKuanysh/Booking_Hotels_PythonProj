from models.filter import  Filter
from models.hotel import Hotel


def get_active_filters(filters: Filter) -> dict:
    print("Active Filters")
    active_filters = {}
    if filters.city:
        active_filters["city"] = filters.city
    active_filters["stars_from"] = filters.stars_from
    active_filters["stars_to"] = filters.stars_to
    if filters.capacity:
        active_filters["capacity"] = filters.capacity
    if filters.room_type:
        active_filters["room_type"] = filters.room_type
    if filters.date_from and filters.date_to:
        active_filters["date_from"] = filters.date_from
        active_filters["date_to"] = filters.date_to
    return active_filters

def get_hotels_by_filters(hotels: dict[int, Hotel], filters: Filter) -> dict[int, Hotel]:
    hotels_by_filters = {}
    f = get_active_filters(filters)




