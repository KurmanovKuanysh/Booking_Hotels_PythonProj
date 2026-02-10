from models.room import Room
from storage import Storage

class RoomsService:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.rooms: dict[int, Room] = storage.load_rooms()

    def get_by_h_id(self, h_id:int) -> dict[int,Room]:
        rooms_in_hotel = {}
        for room in self.rooms.values():
            if room.hotel_id == h_id:
                rooms_in_hotel[room.r_id] = room
        return rooms_in_hotel
    def get_by_id(self, r_id:int) -> Room | None:
        return self.rooms.get(r_id)

