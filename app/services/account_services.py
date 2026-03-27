import os
from enum import Enum

from pwdlib import PasswordHash
from sqlalchemy import Column, Integer, String, Enum as SAEnum
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy import update

DATABASE_URL = os.environ.get("DATABASE_URL","//")

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

class RoleEnum(str, Enum):
    student = "student"
    admin = "admin"

class DBUser(Base):
    __tablename__ = "users"
    
    username = Column(String, primary_key=True, index=True) 
    role = Column(SAEnum(RoleEnum), nullable=False)
    password_hash = Column(String, nullable=False)

pwd_hasher = PasswordHash.recommended()
 

async def changeUserPassword(user_id: int, new_password: str):
    async with AsyncSessionLocal() as session:
        
        hashed_pw = pwd_hasher.hash(new_password)
        
        await session.execute(
            update(DBUser)
            .where(DBUser.id == user_id)
            .values(password_hash=hashed_pw)
        )
        await session.commit()


