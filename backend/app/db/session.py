from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import DB_URL


engine = create_engine(DB_URL, echo=False)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)
