from models.filter import Filter
from models.hotel import Hotel
from models.room import Room
from datetime import date, datetime
from typing import Optional
from services.rooms_service import RoomsService
from models.room_types import RoomType


class FilterService:
    def __init__(self, filters: Filter):
        self.filters = filters

    def set_filter_stars(self, stars_from: int, stars_to: int):
        if stars_from < 1 or stars_to < 1:
            raise Exception("Stars must be greater than 0")
        setattr(self.filters, "stars_from", stars_from)
        setattr(self.filters, "stars_to", stars_to)

    def set_filter_city(self, city: str):
        setattr(self.filters, "city", city)
    def set_filter_capacity(self, capacity: int):
        if capacity < 1:
            raise Exception("Capacity must be greater than 0")
        setattr(self.filters, "capacity", capacity)

    def set_filter_room_type(self, room_type: RoomType):
        if room_type not in ["GENERAL", "FAMILY", "PRESIDENT", "DELUXE"]:
            raise Exception("Invalid room type")
        setattr(self.filters, "room_type", room_type)

    def set_filter_price_range(self, price_from: int, price_to: int):
        setattr(self.filters, "price_from", price_from)
        setattr(self.filters, "price_to", price_to)

    def get_active_filters(self) -> dict:
        active_filters: dict = {}
        if getattr(self.filters, "city", None):
            active_filters["City"] = self.filters.city
        if getattr(self.filters, "stars_from", None):
            active_filters["Stars from"] = self.filters.stars_from
        if getattr(self.filters, "stars_to", None):
            active_filters["Stars to"] = self.filters.stars_to
        if getattr(self.filters, "capacity", None):
            active_filters["Capacity"] = self.filters.capacity
        if getattr(self.filters, "room_type", None):
            active_filters["Room type"] = self.filters.room_type
        if getattr(self.filters, "date_from", None):
            active_filters["Date from"] = self.filters.date_from
        if getattr(self.filters, "date_to", None):
            active_filters["Date to"] = self.filters.date_to
            d_from = self._to_date_(getattr(self.filters, "date_from", None))
            d_to = self._to_date_(getattr(self.filters, "date_to", None))
            if d_from and d_to:
                active_filters["Date from"] = d_from
                active_filters["Date to"] = d_to
        return active_filters
    def get_hotels_by_filters(self, hotels: dict[int, Hotel]) -> dict[int, Hotel]:
        hotels_by_filters: dict[int, Hotel] = {}
        city = getattr(self.filters, "city", None)
        stars_from = getattr(self.filters, "stars_from", None)
        stars_to = getattr(self.filters, "stars_to", None)
        for h_id, h in hotels.items():
            if city and city.strip().lower() not in h.city.strip().lower():
                continue
            if stars_from is not None and h.stars < float(stars_from):
                continue
            if stars_to is not None and h.stars > float(stars_to):
                continue
            hotels_by_filters[h_id] = h

        return hotels_by_filters

    def get_room_by_filter(self, room: Room) -> bool:
        capacity = getattr(self.filters, "capacity", None)
        room_type = getattr(self.filters, "room_type", "GENERAL")
        if capacity is not None:
            if room.capacity < int(capacity):
                return False
        if room_type:
            if room_type.strip().upper() != room.type:
                return False
        return True

    def get_rooms_by_filter(self, rooms: dict[int, Room]) -> dict[int, Room]:
        rooms_by_filter: dict[int, Room] = {}
        for r_id, r in rooms.items():
            if self.get_room_by_filter(r):
                rooms_by_filter[r_id] = r
        return rooms_by_filter

    def _to_date_(self, x) -> Optional[date]:
        if x is None:
            return None
        if isinstance(x, date):
            return x
        if isinstance(x, str):
            return datetime.strptime(x.strip(), "%Y-%m-%d").date()
        raise ValueError(f"Cannot convert {x} to date, unsupported type {type(x)}")

    def filtered_all(self, hotels: dict[int, Hotel], rooms: dict[int, Room], filters: Filter) -> dict[int, Hotel]:
        n_hotel = self.get_hotels_by_filters(hotels)
        check_in = self._to_date_(getattr(filters, "date_from", None))
        check_out = self._to_date_(getattr(filters, "date_to", None))
        f_hotel: dict[int, Hotel] = {}
        for hotel_id, hotel in n_hotel.items():
            is_x = False
            for r in rooms.values():
                if r.hotel_id != hotel_id:
                    continue
                if not self.get_room_by_filter(r):
                    continue
                if check_in and check_out:
                    continue
                if not RoomsService.is_available_rooms(r.r_id, r, check_in, check_out):
                    continue
                is_x = True
                break
            if is_x:
                f_hotel[hotel_id] = hotel
        return f_hotel