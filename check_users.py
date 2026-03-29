import asyncio
from app.core.database import SessionLocal
from sqlalchemy import select
from app.model.models import DBUser

async def get_users():
    async with SessionLocal() as db:
        res = await db.execute(select(DBUser))
        users = res.scalars().all()
        for u in users:
            print(f'User: {u.username}, Role: {u.role.value}')

if __name__ == '__main__':
    asyncio.run(get_users())