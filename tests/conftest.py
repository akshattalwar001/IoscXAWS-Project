import os
import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv

from app.core.database import Base
from app.model.models import DBUser, Student, RoleEnum
from app.services.authHelper import get_password_hash
from main import app

load_dotenv()

# Use test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def test_db():
    """Create a test database and tables."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session_maker() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

@pytest.fixture
async def test_client(test_db):
    """Create a test client with test database."""
    from app.core.database import get_db
    
    async def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()

@pytest.fixture
async def test_user(test_db):
    """Create a test student user."""
    hashed_pwd = await get_password_hash("testpassword")
    user = DBUser(
        username="student1",
        role=RoleEnum.student,
        password_hash=hashed_pwd
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user

@pytest.fixture
async def test_admin(test_db):
    """Create a test admin user."""
    hashed_pwd = await get_password_hash("adminpass")
    admin = DBUser(
        username="admin1",
        role=RoleEnum.admin,
        password_hash=hashed_pwd
    )
    test_db.add(admin)
    await test_db.commit()
    await test_db.refresh(admin)
    return admin

@pytest.fixture
async def test_student(test_db):
    """Create a test student record."""
    student = Student(
        roll_number="2023001",
        name="John Doe",
        branch="CSE",
        year=3,
        email="john@example.com",
        mobile="9876543210"
    )
    test_db.add(student)
    await test_db.commit()
    await test_db.refresh(student)
    return student

@pytest.fixture
async def student_token(test_client, test_user):
    """Get authentication token for student."""
    response = await test_client.post(
        "/auth/token",
        data={"username": "student1", "password": "testpassword"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture
async def admin_token(test_client, test_admin):
    """Get authentication token for admin."""
    response = await test_client.post(
        "/auth/login/admin",
        json={"username": "admin1", "password": "adminpass"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]
