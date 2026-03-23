from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import app.schema.schemas as schemas
import app.model.models as models
from app.services.student_services import get_student_basic


# create academic records for a student
async def create_academic(db: AsyncSession, student_id: int, data: schemas.AcademicCreate):
    await get_student_basic(db, student_id)

    existing = await db.execute(
        select(models.AcademicRecords).where(
            models.AcademicRecords.student_id == student_id
        )
    )

    if existing.scalar_one_or_none():
        raise ValueError("Academic records already exist")

    obj = models.AcademicRecords(
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


# update academic records for a student
async def update_academic(db: AsyncSession, student_id: int, data: schemas.AcademicCreate):
    result = await db.execute(
        select(models.AcademicRecords).where(
            models.AcademicRecords.student_id == student_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Academic records not found")

    for key, value in data.model_dump().items():
        setattr(obj, key, value)

    try:
        await db.commit()
        await db.refresh(obj)
        return obj
    except Exception:
        await db.rollback()
        raise


# get academic records for a student
async def get_academic(db: AsyncSession, student_id: int):
    result = await db.execute(
        select(models.AcademicRecords).where(
            models.AcademicRecords.student_id == student_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Academic records not found")

    return obj