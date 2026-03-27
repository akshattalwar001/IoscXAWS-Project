import os
from enum import Enum

from pwdlib import PasswordHash
from sqlalchemy import Column, Integer, String, Enum as SAEnum
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy import update

from app.core.database import Base, get_db
from app.model.models import DBUser, RoleEnum

pwd_hasher = PasswordHash.recommended()
 

async def changeUserPassword(db: AsyncSession, user_id: int, new_password: str):
    hashed_pw = pwd_hasher.hash(new_password)
    
    await db.execute(
        update(DBUser)
        .where(DBUser.id == user_id)
        .values(password_hash=hashed_pw)
    )
    await db.commit()


