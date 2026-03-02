from app.db.connection import get_conn
from datetime import date
from typing import List, Any

ALLOWED_BOOKING_STATUSES = {"confirmed", "pending", "canceled", "completed"}

def _find_conflict(conn, room_id: int, date_from: date, date_to: date):
    return conn.execute("""
        SELECT 1
        FROM booking b
        WHERE b.r_id = %s
          AND b.status <> 'canceled'
          AND NOT (%s >= b.check_out OR %s <= b.check_in)
        LIMIT 1;
    """, (room_id, date_from, date_to)).fetchone()

def is_room_available(room_id: int, date_from: date, date_to: date) -> bool:
    if date_to <= date_from:
        raise ValueError("date_from must be earlier than date_to")
    with get_conn() as conn:
        return _find_conflict(conn,room_id,date_from,date_to) is None
def create_booking(
        room_id: int,
        user_id: int,
        date_from: date,
        date_to: date,
        status: str = "pending",
) -> int:
    if status not in ALLOWED_BOOKING_STATUSES:
        raise ValueError(f"Invalid status: {status}. Allowed: {sorted(ALLOWED_BOOKING_STATUSES)}")
    if date_to <= date_from:
        raise ValueError("date_from must be earlier than date_to")
    with get_conn() as conn:
        conflict = _find_conflict(conn,room_id,date_from,date_to)
        if conflict is not None:
            raise ValueError("Room is not available for these dates")
        row = conn.execute(
            """
            INSERT INTO booking ( r_id, check_in, check_out, status, user_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (room_id, date_from, date_to, status, user_id)
        ).fetchone()

        return row["id"]
def update_booking_status(booking_id: int, status: str) -> None:
    if status not in ALLOWED_BOOKING_STATUSES:
        raise ValueError("Invalid status")

    with get_conn() as conn:
        row = conn.execute("""
            UPDATE booking
            SET status = %s
            WHERE id = %s
            RETURNING id;
        """, (status, booking_id)).fetchone()

        if row is None:
            raise ValueError("Booking not found")

def list_user_bookings(user_id: int):
    with get_conn() as conn:
        row = conn.execute(
            """
            SELECT
                b.id           AS booking_id,
                b.status       AS status,
                b.check_in     AS check_in,
                b.check_out    AS check_out,
                
                h.id           AS hotel_id,
                h.name         AS hotel_name,
                h.city         AS hotel_city,
                h.stars        AS hotel_stars,
                
                r.id           AS room_id,
                r.room_number  AS room_number,
                rt.type_name   AS room_type_name,
                r.capacity     AS capacity,
                r.price_per_day AS price_per_day,
                r.floor        AS floor
            FROM booking b
            JOIN room r ON r.id = b.r_id
            JOIN room_type rt ON rt.id = r.r_t_id
            JOIN hotels h ON h.id = r.h_id
            WHERE b.user_id = %s
            ORDER BY b.id DESC;
            """,
            (user_id,)
        ).fetchall()

        return row

def cancel_booking(booking_id: int) -> None:
    with get_conn() as conn:
        row = conn.execute("""
            UPDATE booking
            SET status = 'canceled'
            WHERE id = %s
            RETURNING id;
        """,
        (booking_id,)).fetchone()
        if row is None:
            raise ValueError("Booking not found")

def confirm_booking(booking_id: int) -> None:
    with get_conn() as conn:
        row = conn.execute("""
            UPDATE booking
            SET status = 'confirmed'
            WHERE id = %s
            RETURNING id;
        """,
        (booking_id,)).fetchone()
        if row is None:
            raise ValueError("Booking not found")

def complete_booking(booking_id: int) -> None:
    with get_conn() as conn:
        row = conn.execute("""
            UPDATE booking
            SET status = 'completed'
            WHERE id = %s
            RETURNING id;
        """,
        (booking_id,)).fetchone()
        if row is None:
            raise ValueError("Booking not found")

def list_bookings_all() -> list[dict[str, Any]]:
    with get_conn() as conn:
        return conn.execute("""
            SELECT
                u.id          AS user_id,
                u.name        AS user_name,

                b.id          AS booking_id,
                b.status      AS status,
                b.check_in    AS check_in,
                b.check_out   AS check_out,

                h.id          AS hotel_id,
                h.name        AS hotel_name,
                h.city        AS hotel_city,

                r.id          AS room_id,
                r.room_number AS room_number
            FROM booking b
            JOIN users u  ON u.id = b.user_id
            JOIN room r   ON r.id = b.r_id
            JOIN hotels h ON h.id = r.h_id
            ORDER BY b.id DESC;
        """).fetchall()
