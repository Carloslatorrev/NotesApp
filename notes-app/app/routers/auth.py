from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models
from app.config import ALGORITHM, SECRET_KEY
from app.dependencies import get_db
from app.schemas.user import User, UserCreate, UserLogin

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()



def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(models.User).filter(models.User.email == user.email))
    db_user = result.scalars().first()

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(username=user.username, email=user.email)
    new_user.set_password(user.password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user



@router.post("/login")
async def login_for_access_token(form_data: UserLogin, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(models.User).filter(models.User.email == form_data.email))
    user = result.scalars().first()

    if user is None or not user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
