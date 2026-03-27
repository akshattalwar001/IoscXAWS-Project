"""
Create test users (admin1 and student1) for local testing
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.model.models import DBUser, RoleEnum, Base
from app.services.authHelper import get_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Using database: {DATABASE_URL}")

async def create_test_users():
    # Create async engine
    engine = create_async_engine(DATABASE_URL, echo=False)
    
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session_maker() as session:
        # Create admin user
        try:
            admin_pwd = await get_password_hash("adminpass")
            admin = DBUser(
                username="admin1",
                role=RoleEnum.admin,
                password_hash=admin_pwd
            )
            session.add(admin)
            await session.commit()
            print("✓ Created admin user: admin1 / adminpass")
        except Exception as e:
            print(f"Admin user: {e}")
            await session.rollback()
        
        # Create student user
        try:
            student_pwd = await get_password_hash("testpassword")
            student = DBUser(
                username="student1",
                role=RoleEnum.student,
                password_hash=student_pwd
            )
            session.add(student)
            await session.commit()
            print("✓ Created student user: student1 / testpassword")
        except Exception as e:
            print(f"Student user: {e}")
            await session.rollback()
    
    await engine.dispose()
    print("\nTest users created successfully!")
    print("You can now login with:")
    print("  Admin: admin1 / adminpass")
    print("  Student: student1 / testpassword")

if __name__ == "__main__":
    asyncio.run(create_test_users())
