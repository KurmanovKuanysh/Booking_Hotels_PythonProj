from backend.app.db.session import SessionLocal
from backend.app.models.hotel import Hotel
from backend.app.models.room import Room
from backend.app.models.room_type import RoomType
from backend.app.models.booking import Booking
from backend.app.models.user import User
from datetime import date, timedelta

def seed():
    session = SessionLocal()
    try:
        users = [
            User(name="Admin",        email="admin@hotel.com",   password="admin123",  role="ADMIN"),
            User(name="Alice Smith",  email="alice@gmail.com",   password="pass1234",  role="USER"),
            User(name="Bob Johnson",  email="bob@gmail.com",     password="pass5678",  role="USER"),
            User(name="Clara Lee",    email="clara@gmail.com",   password="pass9012",  role="USER"),
            User(name="David Brown",  email="david@gmail.com",   password="pass3456",  role="USER"),
        ]
        session.add_all(users)
        session.flush()

        room_types = [
            RoomType(type_name="general"),
            RoomType(type_name="deluxe"),
            RoomType(type_name="family"),
            RoomType(type_name="suite"),
            RoomType(type_name="president"),
        ]
        session.add_all(room_types)
        session.flush()

        hotels = [
            Hotel(name="Grand Plaza",     city="Moscow",     address="Tverskaya St. 1",      stars=5.0),
            Hotel(name="City Comfort",    city="Saint Petersburg", address="Nevsky Ave. 42", stars=3.5),
            Hotel(name="Sunrise Resort",  city="Sochi",      address="Seaside Blvd. 10",     stars=4.5),
        ]
        session.add_all(hotels)
        session.flush()

        rooms = [
            Room(h_id=hotels[0].id, room_number="101", r_t_id=room_types[0].id, capacity=2,  price_per_day=150.00, floor=1),
            Room(h_id=hotels[0].id, room_number="201", r_t_id=room_types[1].id, capacity=2,  price_per_day=250.00, floor=2),
            Room(h_id=hotels[0].id, room_number="301", r_t_id=room_types[3].id, capacity=4,  price_per_day=500.00, floor=3),
            Room(h_id=hotels[0].id, room_number="401", r_t_id=room_types[4].id, capacity=6,  price_per_day=999.00, floor=4),
            Room(h_id=hotels[1].id, room_number="101", r_t_id=room_types[0].id, capacity=2,  price_per_day=80.00,  floor=1),
            Room(h_id=hotels[1].id, room_number="102", r_t_id=room_types[2].id, capacity=5,  price_per_day=140.00, floor=1),
            Room(h_id=hotels[1].id, room_number="201", r_t_id=room_types[1].id, capacity=2,  price_per_day=120.00, floor=2),
            Room(h_id=hotels[2].id, room_number="101", r_t_id=room_types[0].id, capacity=2,  price_per_day=100.00, floor=1),
            Room(h_id=hotels[2].id, room_number="201", r_t_id=room_types[2].id, capacity=4,  price_per_day=200.00, floor=2),
            Room(h_id=hotels[2].id, room_number="301", r_t_id=room_types[3].id, capacity=3,  price_per_day=350.00, floor=3),
        ]
        session.add_all(rooms)
        session.flush()

        today = date.today()
        bookings = [
            Booking(r_id=rooms[0].id, check_in=today,             check_out=today + timedelta(days=3),  status="confirmed", user_id=users[1].id),
            Booking(r_id=rooms[1].id, check_in=today,             check_out=today + timedelta(days=5),  status="pending",   user_id=users[2].id),
            Booking(r_id=rooms[4].id, check_in=today,             check_out=today + timedelta(days=2),  status="confirmed", user_id=users[3].id),
            Booking(r_id=rooms[7].id, check_in=today,             check_out=today + timedelta(days=7),  status="pending",   user_id=users[4].id),
            Booking(r_id=rooms[2].id, check_in=today + timedelta(days=1), check_out=today + timedelta(days=4),  status="pending",   user_id=users[1].id),
            Booking(r_id=rooms[5].id, check_in=today + timedelta(days=2), check_out=today + timedelta(days=6),  status="confirmed", user_id=users[2].id),
            Booking(r_id=rooms[8].id, check_in=today + timedelta(days=3), check_out=today + timedelta(days=10), status="pending",   user_id=users[3].id),
            Booking(r_id=rooms[3].id, check_in=today + timedelta(days=5), check_out=today + timedelta(days=8),  status="cancelled", user_id=users[4].id),
            Booking(r_id=rooms[9].id, check_in=today + timedelta(days=7), check_out=today + timedelta(days=14), status="pending",  user_id=users[1].id),
            Booking(r_id=rooms[6].id, check_in=today + timedelta(days=10),check_out=today + timedelta(days=12), status="confirmed",user_id=users[2].id),
        ]
        session.add_all(bookings)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    seed()