from models.filter import Filter

def show_active_filters(filters: dict):
    if not filters:
        print("No active filters")
        return
    print("Current Filters:")
    for key, value in filters.items():
        print(f"{key}: {value}")