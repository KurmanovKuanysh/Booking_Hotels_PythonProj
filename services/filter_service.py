from models.filter import  Filter

def show_active_filters(filters: Filter):
    print("Active Filters")

    if filters.city:
        print(f"City: {filters.city}")
    print(f"Stars: {filters.stars_from} - {filters.stars_to}")
    if filters.capacity:
        print(f"Capacity: {filters.capacity} people")
    if filters.room_type:
        print(f"Room type u chose: {filters.room_type}")
    if filters.date_from and filters.date_to:
        print(f"Dates: from {filters.date_from} → to {filters.date_to}")


