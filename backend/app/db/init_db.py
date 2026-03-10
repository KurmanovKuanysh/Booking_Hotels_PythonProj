from backend.app.db.session import engine
from backend.app.db.base import Base


def init_db() -> None:
    Base.metadata.create_all(bind=engine)