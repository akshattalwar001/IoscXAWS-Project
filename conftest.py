"""
Test configuration and fixtures for pytest
"""
import asyncio
import os
from typing import Generator

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.database import Base
from app.model import models
from main import app
from app.core.database import get_db

# Load environment variables for tests
load_dotenv()

# Use test database or in-memory database
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", os.getenv("DATABASE_URL"))


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db() -> AsyncSession:
    """Create a test database session"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
    
    # Cleanup - drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture
async def client(test_db: AsyncSession):
    """Create a test client with database dependency override"""
    async def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Create async client with ASGI transport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    
    # Cleanup
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user_admin(test_db: AsyncSession):
    """Create a test admin user"""
    from app.services.authHelper import create_new_user, RoleEnum
    
    user = await create_new_user(
        test_db,
        username="admin_test",
        plain_password="AdminPassword123",
        role=RoleEnum.admin
    )
    return user


@pytest.fixture
async def test_user_student(test_db: AsyncSession):
    """Create a test student user"""
    from app.services.authHelper import create_new_user, RoleEnum
    
    user = await create_new_user(
        test_db,
        username="student_test",
        plain_password="StudentPassword123",
        role=RoleEnum.student
    )
    return user


@pytest.fixture
async def test_student(test_db: AsyncSession):
    """Create a test student record"""
    student = models.Student(
        roll_number="2023001",
        name="John Doe",
        branch="CSE",
        year=3,
        email="john@example.com",
        mobile="9999999999"
    )
    test_db.add(student)
    await test_db.commit()
    await test_db.refresh(student)
    return student
