from app.db.connection import get_conn
from typing import Any

def list_hotels():
    with get_conn() as conn:
        sql = """
        SELECT id, name, city, address, stars
        FROM hotels
        ORDER BY id
        ;
        """
        res = conn.execute(sql)
        return res.fetchall()

def get_hotel_by_id(hotel_id: int) -> dict[str, Any]:
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT id, name, city, address, stars
            FROM hotels
            WHERE id = %s
            LIMIT 1
            """,
            (hotel_id,)
        ).fetchone()

def find_hotels_by_name(name: str) -> list[dict[str, Any]]:
    name_x = "%" + name + "%"
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT id, name, city, address, stars
            FROM hotels
            WHERE name ILIKE %s
            """,
            (name_x,)
        ).fetchall()

def create_hotel(
        name: str,
        city: str,
        address: str,
        stars: float
):
    with get_conn() as conn:
        row = conn.execute(
            """
            INSERT INTO hotels (name, city, address, stars)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
            """,
            (name, city, address, stars)
        ).fetchone()
        if not row:
            raise Exception("Failed to create hotel")
        return row["id"]

def delete_hotel(hotel_id:int) -> None:
    with get_conn() as conn:
        row = conn.execute(
            """
            DELETE FROM hotels
            WHERE id = %s
            RETURNING id;
            """,
            (hotel_id,)
        ).fetchone()

        if row is None:
            raise ValueError("Hotel not found")

