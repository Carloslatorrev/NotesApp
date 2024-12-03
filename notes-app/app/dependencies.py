from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import SessionLocal, database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        yield db
