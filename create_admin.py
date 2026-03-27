import asyncio
from app.services.authHelper import get_password_hash
from app.core.database import SessionLocal
from app.model.models import DBUser

async def create_admin():
    async with SessionLocal() as session:
        # Create admin
        new_admin = DBUser(
            username='AdminIA100',
            role='admin',
            password_hash=get_password_hash('TcM#7kP$9vL@2wQx'),
            password_changed=True
        )
        session.add(new_admin)
        await session.commit()
        print('Admin created successfully!')
        print('Admin ID: AdminIA100')
        print('Password: TcM#7kP$9vL@2wQx')

asyncio.run(create_admin())
