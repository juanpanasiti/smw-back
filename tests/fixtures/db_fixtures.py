import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.infrastructure.database.models import BaseModel


@pytest.fixture
def sqlite_session():
    # Create SQLite in-memory engine and sessionmaker
    engine = create_engine("sqlite:///:memory:", echo=False, future=True)
    TestingSessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)
    # Create all tables before use
    BaseModel.metadata.create_all(bind=engine)
    return TestingSessionLocal
