import psycopg
from psycopg.rows import dict_row
from contextlib import contextmanager
from app.core.config import DB_URL


@contextmanager
def get_conn():
    conn = psycopg.connect(DB_URL, row_factory=dict_row)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
