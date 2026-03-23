from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import app.model.models as models
import app.schema.schemas as schemas
from app.services.student_services import get_student_basic


# create research paper
async def create_research(db: AsyncSession, student_id: int, data: schemas.ResearchCreate):
    await get_student_basic(db, student_id)

    obj = models.ResearchPaper(
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


# get all research papers for a student
async def get_research(db: AsyncSession, student_id: int):
    result = await db.execute(
        select(models.ResearchPaper).where(
            models.ResearchPaper.student_id == student_id
        )
    )
    return result.scalars().all()


# update research paper
async def update_research(db: AsyncSession, paper_id: int, data: schemas.ResearchCreate):
    result = await db.execute(
        select(models.ResearchPaper).where(
            models.ResearchPaper.id == paper_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Research paper not found")

    for key, value in data.model_dump().items():
        setattr(obj, key, value)

    try:
        await db.commit()
        await db.refresh(obj)
        return obj
    except Exception:
        await db.rollback()
        raise


# delete research paper
async def delete_research(db: AsyncSession, paper_id: int):
    result = await db.execute(
        select(models.ResearchPaper).where(
            models.ResearchPaper.id == paper_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Research paper not found")

    try:
        await db.delete(obj)
        await db.commit()
        return {"detail": "Research paper deleted"}
    except Exception:
        await db.rollback()
        raise