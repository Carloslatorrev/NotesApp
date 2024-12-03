import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import Base


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/notes_app"


engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def init_db():

    with engine.begin() as conn:
        conn.run_sync(Base.metadata.drop_all)
        conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
def setup_db():
    init_db()
    yield

    with engine.begin() as conn:
        conn.run_sync(Base.metadata.drop_all)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

