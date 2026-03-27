from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import app.schema.schemas as schemas
from app.services.student_services import get_student_basic
import app.model.models as models


# Create a new parent details entry for a student
async def create_parent(db: AsyncSession, student_id: str, data: schemas.ParentCreate):
    await get_student_basic(db, student_id)
    existing = await db.execute(
        select(models.ParentDetails).where(
            models.ParentDetails.student_id == student_id
        )
    )
    if existing.scalar_one_or_none():
        raise ValueError("Parent details already exist")
    obj = models.ParentDetails(
        student_id=student_id,
        **data.model_dump()
    )
    db.add(obj)
    try:
        await db.commit()
        await db.refresh(obj)
        return obj
    except Exception:
        await db.rollback()
        raise


# Update parent details for a student
async def update_parent(db: AsyncSession, student_id: str, data: schemas.ParentCreate):
    result = await db.execute(
        select(models.ParentDetails).where(
            models.ParentDetails.student_id == student_id
        )
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise ValueError("Parent details not found")
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    try:
        await db.commit()
        await db.refresh(obj)
        return obj
    except Exception:
        await db.rollback()
        raise


# Get parent details for a student
async def get_parent(db: AsyncSession, student_id: str):
    result = await db.execute(
        select(models.ParentDetails).where(
            models.ParentDetails.student_id == student_id
        )
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise ValueError("Parent details not found")
    return obj
