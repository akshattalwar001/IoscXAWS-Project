import os
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Enum as SAEnum
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.future import select

from app.core.database import Base, get_db
from app.model.models import DBUser

class RoleEnum(str, Enum):
    student = "student"
    admin = "admin"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int

class LoginRequest(BaseModel):
    username: str
    password: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class User(BaseModel):
    id: int
    username: str
    role: RoleEnum
    
    class Config:
        from_attributes = True

SECRET_KEY = "caf5b0f96c9f718b4d38162bcea267342ed871815cc1aac8cad63b7bf1858467"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

async def get_password_hash(password):
    return password_hash.hash(password)

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(DBUser).filter(DBUser.username== username))
    return result.scalars().first()

async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(DBUser).filter(DBUser.id == user_id))
    return result.scalars().first()

async def create_new_user(db: AsyncSession, username: str, plain_password: str, role: RoleEnum):
    hashed_pwd = await get_password_hash(plain_password)
    db_user = DBUser(username=username, role=role, password_hash=hashed_pwd)
    db.add(db_user)
    await  db.commit()
    await db.refresh(db_user)
    return db_user

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return False
    if not await verify_password(password, user.password_hash):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = str(payload.get("sub"))
        
        if user_id_str is None:
            raise credentials_exception
            
        token_data = TokenData(id=int(user_id_str))
        
    except (InvalidTokenError, ValueError):
        raise credentials_exception
        
    user = await get_user_by_id(db, user_id=token_data.id)
    if user is None:
        raise credentials_exception
        
    return user
