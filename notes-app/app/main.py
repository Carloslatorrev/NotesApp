# app/main.py
import os

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import database
from app.routers import auth, notes

app = FastAPI()

os.environ['TEST_ENV'] = 'False'

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(notes.router, tags=["notes"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
