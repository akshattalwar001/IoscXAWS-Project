from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import app.model.models as models
import app.schema.schemas as schemas
from app.services.student_services import get_student_basic
from app.services.file_services import save_file


# create a new documents record for a student
async def create_documents(db: AsyncSession, student_id: int, data: schemas.DocumentsCreate):
    await get_student_basic(db, student_id)

    existing = await db.execute(
        select(models.Documents).where(
            models.Documents.student_id == student_id
        )
    )

    if existing.scalar_one_or_none():
        raise ValueError("Documents record already exists")

    obj = models.Documents(
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


# update existing documents record for a student
async def update_documents(db: AsyncSession, student_id: int, data: schemas.DocumentsCreate):
    result = await db.execute(
        select(models.Documents).where(
            models.Documents.student_id == student_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Documents not found")

    for key, value in data.model_dump().items():
        setattr(obj, key, value)

    try:
        await db.commit()
        await db.refresh(obj)
        return obj
    except Exception:
        await db.rollback()
        raise


# get documents for a student
async def get_documents(db: AsyncSession, student_id: int):
    result = await db.execute(
        select(models.Documents).where(
            models.Documents.student_id == student_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Documents not found")

    return obj


# upload document files for a student
async def upload_documents(
    db: AsyncSession,
    student_id: int,
    aadhaar=None,
    pan=None,
    id_card=None
):
    result = await db.execute(
        select(models.Documents).where(
            models.Documents.student_id == student_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Documents record not found. Create it first.")

    if aadhaar:
        obj.aadhaar_path = save_file(student_id, aadhaar)
    if pan:
        obj.pan_path = save_file(student_id, pan)
    if id_card:
        obj.id_card_path = save_file(student_id, id_card)

    try:
        await db.commit()
        return {
            "aadhaar_path": obj.aadhaar_path,
            "pan_path": obj.pan_path,
            "id_card_path": obj.id_card_path
        }
    except Exception:
        await db.rollback()
        raise