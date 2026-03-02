from app.db.connection import get_conn
from datetime import date

def clear() -> None:
    with get_conn() as conn:
        conn.execute("TRUNCATE TABLE booking RESTART IDENTITY CASCADE;")
        conn.execute("TRUNCATE TABLE room RESTART IDENTITY CASCADE;")
        conn.execute("TRUNCATE TABLE room_type RESTART IDENTITY CASCADE;")
        conn.execute("TRUNCATE TABLE hotels RESTART IDENTITY CASCADE;")
        conn.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE;")

def seed_room_types() -> None:
    types = [
        ('GENERAL',),
        ('DELUXE',),
        ('SUITE',),
        ('FAMILY',),
        ('PRESIDENT',),
    ]
    with get_conn() as conn:
        for t in types:
            conn.execute("""
                INSERT INTO room_type (type_name)
                   VALUES (%s)
                """,
                t
            )

def seed_hotel() -> None:
    hotel_list =[
        ('Main Resort', 'Karaganda', 'Abaya 1', 4.0)
    ]

    with get_conn() as conn:
        for hotel in hotel_list:
            conn.execute("""
                INSERT INTO hotels (name, city, address, stars)
                VALUES (%s, %s, %s, %s)
                """,
                hotel
            )
def seed_user() -> None:
    user_list = [
        ('John Doe', 'john.doe@example.com', 'password123', 'USER')
    ]

    with get_conn() as conn:
        for u in user_list:
            conn.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, %s)
            """,
            u
            )
def seed_rooms() -> None:
    with get_conn() as conn:

        hotel_id = conn.execute("""
            SELECT id FROM hotels
            WHERE name = 'Main Resort'
        """).fetchone()["id"]

        types = conn.execute("""
            SELECT id, type_name FROM room_type
        """).fetchall()

        type_map = {t["type_name"]: t["id"] for t in types}

        rooms = [
            (hotel_id, "101", type_map["GENERAL"], 2, 20000, 1),
            (hotel_id, "102", type_map["DELUXE"], 3, 35000, 1),
            (hotel_id, "201", type_map["SUITE"], 4, 60000, 2),
        ]

        for r in rooms:
            conn.execute("""
                INSERT INTO room
                (h_id, room_number, r_t_id, capacity, price_per_day, floor)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, r)

def seed_bookings() -> None:
    with get_conn() as conn:
        room_id = conn.execute("""
            SELECT id FROM room
            WHERE room_number = '101'
            LIMIT 1
        """).fetchone()["id"]

        user_id = conn.execute("""
            SELECT id FROM users
            WHERE email = 'john.doe@example.com'
        """).fetchone()["id"]

        conn.execute("""
            INSERT INTO booking
            (r_id, check_in, check_out, status, user_id)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            room_id,
            date(2026, 3, 10),
            date(2026, 3, 15),
            "confirmed",
            user_id
        ))



def run() -> None:
    clear()
    seed_room_types()
    seed_hotel()
    seed_user()
    seed_rooms()
    seed_bookings()
    print("Database seeded successfully")

if __name__ == "__main__":
    run()