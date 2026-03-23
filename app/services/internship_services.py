from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import app.model.models as models
import app.schema.schemas as schemas
from app.services.student_services import get_student_basic


# Create a new internship for a student
async def create_internship(db: AsyncSession, student_id: int, data: schemas.InternshipCreate):
    await get_student_basic(db, student_id)

    obj = models.Internship(
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


# get all internships for a student
async def get_internships(db: AsyncSession, student_id: int):
    result = await db.execute(
        select(models.Internship).where(
            models.Internship.student_id == student_id
        )
    )
    return result.scalars().all()


# Update an internship
async def update_internship(db: AsyncSession, internship_id: int, data: schemas.InternshipCreate):
    result = await db.execute(
        select(models.Internship).where(
            models.Internship.id == internship_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Internship not found")

    for key, value in data.model_dump().items():
        setattr(obj, key, value)

    try:
        await db.commit()
        await db.refresh(obj)
        return obj
    except Exception:
        await db.rollback()
        raise


# delete an internship
async def delete_internship(db: AsyncSession, internship_id: int):
    result = await db.execute(
        select(models.Internship).where(
            models.Internship.id == internship_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Internship not found")

    try:
        await db.delete(obj)
        await db.commit()
        return {"detail": "Internship deleted"}
    except Exception:
        await db.rollback()
        raise