import os
from enum import Enum

from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update

from app.core.database import Base, get_db
from app.model.models import DBUser, RoleEnum, ParentDetails

pwd_hasher = PasswordHash.recommended()


async def changeUserPassword(db: AsyncSession, user_id: int, new_password: str):
    hashed_pw = pwd_hasher.hash(new_password)
    await db.execute(
        update(DBUser)
        .where(DBUser.id == user_id)
        .values(password_hash=hashed_pw)
    )
    await db.commit()


async def resetPasswordToDefault(db: AsyncSession, student_id: str):
    result = await db.execute(
        select(ParentDetails).where(ParentDetails.student_id == student_id)
    )
    parent = result.scalar_one_or_none()
    if not parent:
        raise ValueError("Parent details not found for this student")

    hashed_pw = pwd_hasher.hash(parent.parent_name)

    await db.execute(
        update(DBUser)
        .where(DBUser.username == student_id)
        .values(password_hash=hashed_pw, password_changed=False)
    )
    await db.commit()
    