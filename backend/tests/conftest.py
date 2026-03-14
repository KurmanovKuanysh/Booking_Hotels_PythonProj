import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.app.db.base import Base
import os
from dotenv import load_dotenv

from backend.app.models import User, Booking, Hotel, Room, RoomType

load_dotenv()
DB_NAME = os.getenv('TEST_DB_NAME', 'booking_test')
DB_USER = os.getenv('TEST_DB_USER', 'postgres')
DB_PASSWORD = os.getenv('TEST_DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('TEST_DB_HOST', 'localhost')
DB_PORT = os.getenv('TEST_DB_PORT', '5432')

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL, echo=False)
TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def session():
    connection = engine.connect()
    transaction = connection.begin()

    session: Session = TestSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()