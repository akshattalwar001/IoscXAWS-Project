from sqlalchemy import select       
from sqlalchemy.ext.asyncio import AsyncSession
import app.schema.schemas as schemas
import app.model.models as models
from app.services.student_services import get_student_basic


# Create financial info for a student
async def create_financial(db: AsyncSession, student_id: int, data: schemas.FinancialCreate):
    await get_student_basic(db, student_id)

    existing = await db.execute(
        select(models.FinancialInfo).where(
            models.FinancialInfo.student_id == student_id
        )
    )

    if existing.scalar_one_or_none():
        raise ValueError("Financial info already exists")

    obj = models.FinancialInfo(
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


# Update financial info for a student
async def update_financial(db: AsyncSession, student_id: int, data: schemas.FinancialCreate):
    result = await db.execute(
        select(models.FinancialInfo).where(
            models.FinancialInfo.student_id == student_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Financial info not found")

    for key, value in data.model_dump().items():
        setattr(obj, key, value)

    try:
        await db.commit()
        await db.refresh(obj)
        return obj
    except Exception:
        await db.rollback()
        raise


# Get financial info for a student
async def get_financial(db: AsyncSession, student_id: int):
    result = await db.execute(
        select(models.FinancialInfo).where(
            models.FinancialInfo.student_id == student_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Financial info not found")

    return obj