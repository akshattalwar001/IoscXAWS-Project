from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import app.schema.schemas as schemas
import app.model.models as models
from app.services.student_services import get_student_basic


# create a new classification for a student
async def create_classification(db: AsyncSession, student_id: str, data: schemas.ClassificationCreate):
    await get_student_basic(db, student_id)

    existing = await db.execute(
        select(models.StudentClassification).where(
            models.StudentClassification.student_id == student_id
        )
    )

    if existing.scalar_one_or_none():
        raise ValueError("Classification already exists")

    obj = models.StudentClassification(
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


# update an existing classification for a student
async def update_classification(db: AsyncSession, student_id: str, data: schemas.ClassificationCreate):
    result = await db.execute(
        select(models.StudentClassification).where(
            models.StudentClassification.student_id == student_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Classification not found")

    for key, value in data.model_dump().items():
        setattr(obj, key, value)

    try:
        await db.commit()
        await db.refresh(obj)
        return obj
    except Exception:
        await db.rollback()
        raise


# get the classification for a student
async def get_classification(db: AsyncSession, student_id: str):
    result = await db.execute(
        select(models.StudentClassification).where(
            models.StudentClassification.student_id == student_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Classification not found")

    return obj
