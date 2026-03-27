from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import app.model.models as models
import app.schema.schemas as schemas
from app.services.student_services import get_student_basic
from app.services.file_services import save_file


# create academic documents record for a student    
async def create_academic_docs(db: AsyncSession, student_id: str, data: schemas.AcademicDocsCreate):
    await get_student_basic(db, student_id)

    existing = await db.execute(
        select(models.AcademicDocuments).where(
            models.AcademicDocuments.student_id == student_id
        )
    )

    if existing.scalar_one_or_none():
        raise ValueError("Academic documents record already exists")

    obj = models.AcademicDocuments(
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


# update academic documents record for a student
async def update_academic_docs(db: AsyncSession, student_id: str, data: schemas.AcademicDocsCreate):
    result = await db.execute(
        select(models.AcademicDocuments).where(
            models.AcademicDocuments.student_id == student_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Academic documents not found")

    for key, value in data.model_dump().items():
        setattr(obj, key, value)

    try:
        await db.commit()
        await db.refresh(obj)
        return obj
    except Exception:
        await db.rollback()
        raise


# get academic documents record for a student
async def get_academic_docs(db: AsyncSession, student_id: str):
    result = await db.execute(
        select(models.AcademicDocuments).where(
            models.AcademicDocuments.student_id == student_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Academic documents not found")

    return obj


# upload academic documents files for a student
async def upload_academic_docs(
    db: AsyncSession,
    student_id: str,
    marksheets=None,
    provisional_cert=None
):
    result = await db.execute(
        select(models.AcademicDocuments).where(
            models.AcademicDocuments.student_id == student_id
        )
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise ValueError("Academic documents record not found. Create it first.")

    if marksheets:
        obj.marksheets_path = save_file(student_id, marksheets)
    if provisional_cert:
        obj.provisional_cert_path = save_file(student_id, provisional_cert)

    try:
        await db.commit()
        return {
            "marksheets_path": obj.marksheets_path,
            "provisional_cert_path": obj.provisional_cert_path
        }
    except Exception:
        await db.rollback()
        raise
