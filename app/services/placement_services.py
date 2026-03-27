from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import app.model.models as models
import app.schema.schemas as schemas
from app.services.student_services import get_student_basic


# create new placement record for a student
async def create_placement(db: AsyncSession, student_id: str, data: schemas.PlacementCreate):
    await get_student_basic(db, student_id)

    existing = await db.execute(
        select(models.Placement).where(
            models.Placement.student_id == student_id
        )
    )

    if existing.scalar_one_or_none():
        raise ValueError("Placement record already exists")

    obj = models.Placement(
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


# update existing placement record for a student
async def update_placement(db: AsyncSession, student_id: str, data: schemas.PlacementCreate):
    result = await db.execute(
        select(models.Placement).where(
            models.Placement.student_id == student_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Placement record not found")

    for key, value in data.model_dump().items():
        setattr(obj, key, value)

    try:
        await db.commit()
        await db.refresh(obj)
        return obj
    except Exception:
        await db.rollback()
        raise


# get placement record for a student
async def get_placement(db: AsyncSession, student_id: str):
    result = await db.execute(
        select(models.Placement).where(
            models.Placement.student_id == student_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Placement record not found")

    return obj
