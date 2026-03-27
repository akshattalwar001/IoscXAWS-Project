from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import app.model.models as models
from sqlalchemy.orm import selectinload
import app.schema.schemas as schemas
from app.services.file_services import save_file


# get student basic
async def get_student_basic(db: AsyncSession, student_id: str):
    result = await db.execute(
        select(models.Student).where(models.Student.roll_number == student_id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise ValueError("Student not found")
    return student


# get student full profile
async def get_student_full(db: AsyncSession, student_id: str):
    result = await db.execute(
        select(models.Student)
        .where(models.Student.roll_number == student_id)
        .options(
            selectinload(models.Student.classification),
            selectinload(models.Student.parent_details),
            selectinload(models.Student.academic_records),
            selectinload(models.Student.financial_info),
            selectinload(models.Student.documents),
            selectinload(models.Student.noc_records),
            selectinload(models.Student.placement),
            selectinload(models.Student.academic_documents),
            selectinload(models.Student.internships),
            selectinload(models.Student.research_papers),
        )
    )
    student = result.scalar_one_or_none()
    if not student:
        raise ValueError("Student not found")
    return student


# create new student
async def create_student(db: AsyncSession, student_data):
    student = models.Student(**student_data.model_dump())
    db.add(student)
    try:
        await db.commit()
        await db.refresh(student)
        return student
    except Exception:
        await db.rollback()
        raise


# ------------------ LIST ------------------
async def list_students(db: AsyncSession, branch=None, year=None):
    query = select(models.Student)

    if branch:
        query = query.where(models.Student.branch == branch)
    if year:
        query = query.where(models.Student.year == year)

    result = await db.execute(query)
    return result.scalars().all()


# update existing student
async def update_student(db: AsyncSession, student_id: str, data: schemas.StudentUpdate):
    student = await get_student_basic(db, student_id)

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(student, key, value)

    try:
        await db.commit()
        await db.refresh(student)
        return student
    except Exception:
        await db.rollback()
        raise


# delete student
async def delete_student(db: AsyncSession, student_id: str):
    student = await get_student_basic(db, student_id)

    try:
        await db.delete(student)
        await db.commit()
        return {"detail": "Student deleted"}
    except Exception:
        await db.rollback()
        raise


# upload photo
async def upload_photo(db: AsyncSession, student_id: str, photo):
    student = await get_student_basic(db, student_id)

    student.photo_path = save_file(student_id, photo)

    try:
        await db.commit()
        return {"photo_path": student.photo_path}
    except Exception:
        await db.rollback()
        raise

# upload signature
async def upload_signature(db: AsyncSession, student_id: str, signature):
    student = await get_student_basic(db, student_id)

    student.signature_path = save_file(student_id, signature)

    try:
        await db.commit()
        return {"signature_path": student.signature_path}
    except Exception:
        await db.rollback()
        raise
