from app.db.connection import get_conn
from typing import Any


BASE_ROOMS = """
    SELECT
        r.id AS room_id,
        r.h_id AS hotel_id,
        r.room_number,
        rt.id AS type_id,
        rt.type_name,
        r.capacity,
        r.price_per_day,
        r.floor
    FROM room r
    JOIN room_type rt ON rt.id = r.r_t_id
"""


def list_rooms_all() -> list[dict[str, Any]]:
    with get_conn() as conn:
        return conn.execute(
            BASE_ROOMS + " ORDER BY r.id;"
        ).fetchall()

def list_rooms_by_hotel_id(h_id: int) -> list[dict[str, Any]]:
    with get_conn() as conn:
        return conn.execute(
            BASE_ROOMS + """
            WHERE r.h_id = %s
            ORDER BY r.id;
            """,
            (h_id,)
        ).fetchall()