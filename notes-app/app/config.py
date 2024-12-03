import os

from databases import Database
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"


class Settings(BaseSettings):

    database_url: str
    test_database_url: str

    class Config:
        env_file = ".env"


settings = Settings()

DATABASE_URL = settings.test_database_url if os.getenv('TEST_ENV', False) else settings.database_url

engine = create_async_engine(DATABASE_URL, echo=True)


SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, class_=AsyncSession, bind=engine
)


database = Database(DATABASE_URL)


Base = declarative_base()
