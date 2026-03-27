from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import app.model.models as models
import app.schema.schemas as schemas
from app.services.student_services import get_student_basic


# create a new NOC record for a student
async def create_noc(db: AsyncSession, student_id: str, data: schemas.NocCreate):
    await get_student_basic(db, student_id)

    existing = await db.execute(
        select(models.NocRecords).where(
            models.NocRecords.student_id == student_id
        )
    )

    if existing.scalar_one_or_none():
        raise ValueError("NOC record already exists")

    obj = models.NocRecords(
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


# update existing NOC record for a student
async def update_noc(db: AsyncSession, student_id: str, data: schemas.NocCreate):
    result = await db.execute(
        select(models.NocRecords).where(
            models.NocRecords.student_id == student_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("NOC record not found")

    for key, value in data.model_dump().items():
        setattr(obj, key, value)

    try:
        await db.commit()
        await db.refresh(obj)
        return obj
    except Exception:
        await db.rollback()
        raise


# get NOC record for a student
async def get_noc(db: AsyncSession, student_id: str):
    result = await db.execute(
        select(models.NocRecords).where(
            models.NocRecords.student_id == student_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("NOC record not found")

    return obj
