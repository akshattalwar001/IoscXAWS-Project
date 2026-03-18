import os
import shutil
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func

from database import get_db
import models
import schemas

router = APIRouter()
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")


def save_file(student_id: int, file: UploadFile) -> str:
    folder = os.path.join(UPLOAD_DIR, str(student_id))
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, file.filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return path


async def get_student_or_404(student_id: int, db: AsyncSession):
    result = await db.execute(select(models.Student).where(models.Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# ── Students ──────────────────────────────────────────────────────────────────

@router.post("/students", response_model=schemas.StudentResponse, tags=["Students"])
async def create_student(student: schemas.StudentCreate, db: AsyncSession = Depends(get_db)):
    new_student = models.Student(**student.model_dump())
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return new_student


@router.get("/students", response_model=List[schemas.StudentResponse], tags=["Students"])
async def list_students(
    branch: Optional[str] = None,
    year: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(models.Student)
    if branch:
        query = query.where(models.Student.branch == branch)
    if year:
        query = query.where(models.Student.year == year)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/students/{student_id}", response_model=schemas.FullStudentProfile, tags=["Students"])
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Student)
        .where(models.Student.id == student_id)
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
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/students/{student_id}", response_model=schemas.StudentResponse, tags=["Students"])
async def update_student(student_id: int, data: schemas.StudentUpdate, db: AsyncSession = Depends(get_db)):
    student = await get_student_or_404(student_id, db)
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(student, key, value)
    await db.commit()
    await db.refresh(student)
    return student


@router.delete("/students/{student_id}", tags=["Students"])
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await get_student_or_404(student_id, db)
    await db.delete(student)
    await db.commit()
    return {"detail": "Student deleted"}


# ── Photo / Signature uploads ─────────────────────────────────────────────────

@router.post("/students/{student_id}/photo", tags=["Students"])
async def upload_photo(student_id: int, photo: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    student = await get_student_or_404(student_id, db)
    student.photo_path = save_file(student_id, photo)
    await db.commit()
    return {"photo_path": student.photo_path}


@router.post("/students/{student_id}/signature", tags=["Students"])
async def upload_signature(student_id: int, signature: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    student = await get_student_or_404(student_id, db)
    student.signature_path = save_file(student_id, signature)
    await db.commit()
    return {"signature_path": student.signature_path}


# ── Classification ────────────────────────────────────────────────────────────

@router.post("/students/{student_id}/classification", response_model=schemas.ClassificationResponse, tags=["Classification"])
async def create_classification(student_id: int, data: schemas.ClassificationCreate, db: AsyncSession = Depends(get_db)):
    await get_student_or_404(student_id, db)
    existing = await db.execute(select(models.StudentClassification).where(models.StudentClassification.student_id == student_id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Classification already exists")
    obj = models.StudentClassification(student_id=student_id, **data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/students/{student_id}/classification", response_model=schemas.ClassificationResponse, tags=["Classification"])
async def update_classification(student_id: int, data: schemas.ClassificationCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.StudentClassification).where(models.StudentClassification.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Classification not found")
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/students/{student_id}/classification", response_model=schemas.ClassificationResponse, tags=["Classification"])
async def get_classification(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.StudentClassification).where(models.StudentClassification.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Classification not found")
    return obj


# ── Academic Records ──────────────────────────────────────────────────────────

@router.post("/students/{student_id}/academic", response_model=schemas.AcademicResponse, tags=["Academic"])
async def create_academic(student_id: int, data: schemas.AcademicCreate, db: AsyncSession = Depends(get_db)):
    await get_student_or_404(student_id, db)
    existing = await db.execute(select(models.AcademicRecords).where(models.AcademicRecords.student_id == student_id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Academic records already exist")
    obj = models.AcademicRecords(student_id=student_id, **data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/students/{student_id}/academic", response_model=schemas.AcademicResponse, tags=["Academic"])
async def update_academic(student_id: int, data: schemas.AcademicCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.AcademicRecords).where(models.AcademicRecords.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Academic records not found")
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/students/{student_id}/academic", response_model=schemas.AcademicResponse, tags=["Academic"])
async def get_academic(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.AcademicRecords).where(models.AcademicRecords.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Academic records not found")
    return obj


# ── Parent Details ────────────────────────────────────────────────────────────

@router.post("/students/{student_id}/parent", response_model=schemas.ParentResponse, tags=["Parent"])
async def create_parent(student_id: int, data: schemas.ParentCreate, db: AsyncSession = Depends(get_db)):
    await get_student_or_404(student_id, db)
    existing = await db.execute(select(models.ParentDetails).where(models.ParentDetails.student_id == student_id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Parent details already exist")
    obj = models.ParentDetails(student_id=student_id, **data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/students/{student_id}/parent", response_model=schemas.ParentResponse, tags=["Parent"])
async def update_parent(student_id: int, data: schemas.ParentCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.ParentDetails).where(models.ParentDetails.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Parent details not found")
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/students/{student_id}/parent", response_model=schemas.ParentResponse, tags=["Parent"])
async def get_parent(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.ParentDetails).where(models.ParentDetails.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Parent details not found")
    return obj


# ── Financial Info ────────────────────────────────────────────────────────────

@router.post("/students/{student_id}/financial", response_model=schemas.FinancialResponse, tags=["Financial"])
async def create_financial(student_id: int, data: schemas.FinancialCreate, db: AsyncSession = Depends(get_db)):
    await get_student_or_404(student_id, db)
    existing = await db.execute(select(models.FinancialInfo).where(models.FinancialInfo.student_id == student_id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Financial info already exists")
    obj = models.FinancialInfo(student_id=student_id, **data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/students/{student_id}/financial", response_model=schemas.FinancialResponse, tags=["Financial"])
async def update_financial(student_id: int, data: schemas.FinancialCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.FinancialInfo).where(models.FinancialInfo.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Financial info not found")
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/students/{student_id}/financial", response_model=schemas.FinancialResponse, tags=["Financial"])
async def get_financial(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.FinancialInfo).where(models.FinancialInfo.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Financial info not found")
    return obj


# ── Internships ───────────────────────────────────────────────────────────────

@router.post("/students/{student_id}/internships", response_model=schemas.InternshipResponse, tags=["Internships"])
async def create_internship(student_id: int, data: schemas.InternshipCreate, db: AsyncSession = Depends(get_db)):
    await get_student_or_404(student_id, db)
    obj = models.Internship(student_id=student_id, **data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/students/{student_id}/internships", response_model=List[schemas.InternshipResponse], tags=["Internships"])
async def get_internships(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Internship).where(models.Internship.student_id == student_id))
    return result.scalars().all()


@router.put("/internships/{internship_id}", response_model=schemas.InternshipResponse, tags=["Internships"])
async def update_internship(internship_id: int, data: schemas.InternshipCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Internship).where(models.Internship.id == internship_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Internship not found")
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/internships/{internship_id}", tags=["Internships"])
async def delete_internship(internship_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Internship).where(models.Internship.id == internship_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Internship not found")
    await db.delete(obj)
    await db.commit()
    return {"detail": "Internship deleted"}


# ── Research Papers ───────────────────────────────────────────────────────────

@router.post("/students/{student_id}/research", response_model=schemas.ResearchResponse, tags=["Research"])
async def create_research(student_id: int, data: schemas.ResearchCreate, db: AsyncSession = Depends(get_db)):
    await get_student_or_404(student_id, db)
    obj = models.ResearchPaper(student_id=student_id, **data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/students/{student_id}/research", response_model=List[schemas.ResearchResponse], tags=["Research"])
async def get_research(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.ResearchPaper).where(models.ResearchPaper.student_id == student_id))
    return result.scalars().all()


@router.put("/research/{paper_id}", response_model=schemas.ResearchResponse, tags=["Research"])
async def update_research(paper_id: int, data: schemas.ResearchCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.ResearchPaper).where(models.ResearchPaper.id == paper_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Research paper not found")
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/research/{paper_id}", tags=["Research"])
async def delete_research(paper_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.ResearchPaper).where(models.ResearchPaper.id == paper_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Research paper not found")
    await db.delete(obj)
    await db.commit()
    return {"detail": "Research paper deleted"}


# ── Documents ─────────────────────────────────────────────────────────────────

@router.post("/students/{student_id}/documents", response_model=schemas.DocumentsResponse, tags=["Documents"])
async def create_documents(student_id: int, data: schemas.DocumentsCreate, db: AsyncSession = Depends(get_db)):
    await get_student_or_404(student_id, db)
    existing = await db.execute(select(models.Documents).where(models.Documents.student_id == student_id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Documents record already exists")
    obj = models.Documents(student_id=student_id, **data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/students/{student_id}/documents", response_model=schemas.DocumentsResponse, tags=["Documents"])
async def update_documents(student_id: int, data: schemas.DocumentsCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Documents).where(models.Documents.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Documents not found")
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/students/{student_id}/documents", response_model=schemas.DocumentsResponse, tags=["Documents"])
async def get_documents(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Documents).where(models.Documents.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Documents not found")
    return obj


@router.post("/students/{student_id}/documents/upload", tags=["Documents"])
async def upload_documents(
    student_id: int,
    aadhaar: Optional[UploadFile] = File(None),
    pan: Optional[UploadFile] = File(None),
    id_card: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.Documents).where(models.Documents.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Documents record not found. Create it first.")
    if aadhaar:
        obj.aadhaar_path = save_file(student_id, aadhaar)
    if pan:
        obj.pan_path = save_file(student_id, pan)
    if id_card:
        obj.id_card_path = save_file(student_id, id_card)
    await db.commit()
    return {"aadhaar_path": obj.aadhaar_path, "pan_path": obj.pan_path, "id_card_path": obj.id_card_path}


# ── NOC Records ───────────────────────────────────────────────────────────────

@router.post("/students/{student_id}/noc", response_model=schemas.NocResponse, tags=["NOC"])
async def create_noc(student_id: int, data: schemas.NocCreate, db: AsyncSession = Depends(get_db)):
    await get_student_or_404(student_id, db)
    existing = await db.execute(select(models.NocRecords).where(models.NocRecords.student_id == student_id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="NOC record already exists")
    obj = models.NocRecords(student_id=student_id, **data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/students/{student_id}/noc", response_model=schemas.NocResponse, tags=["NOC"])
async def update_noc(student_id: int, data: schemas.NocCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.NocRecords).where(models.NocRecords.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="NOC record not found")
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/students/{student_id}/noc", response_model=schemas.NocResponse, tags=["NOC"])
async def get_noc(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.NocRecords).where(models.NocRecords.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="NOC record not found")
    return obj


# ── Placement ─────────────────────────────────────────────────────────────────

@router.post("/students/{student_id}/placement", response_model=schemas.PlacementResponse, tags=["Placement"])
async def create_placement(student_id: int, data: schemas.PlacementCreate, db: AsyncSession = Depends(get_db)):
    await get_student_or_404(student_id, db)
    existing = await db.execute(select(models.Placement).where(models.Placement.student_id == student_id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Placement record already exists")
    obj = models.Placement(student_id=student_id, **data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/students/{student_id}/placement", response_model=schemas.PlacementResponse, tags=["Placement"])
async def update_placement(student_id: int, data: schemas.PlacementCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Placement).where(models.Placement.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Placement record not found")
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/students/{student_id}/placement", response_model=schemas.PlacementResponse, tags=["Placement"])
async def get_placement(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Placement).where(models.Placement.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Placement record not found")
    return obj


# ── Academic Documents ────────────────────────────────────────────────────────

@router.post("/students/{student_id}/academic-documents", response_model=schemas.AcademicDocsResponse, tags=["Academic Documents"])
async def create_academic_docs(student_id: int, data: schemas.AcademicDocsCreate, db: AsyncSession = Depends(get_db)):
    await get_student_or_404(student_id, db)
    existing = await db.execute(select(models.AcademicDocuments).where(models.AcademicDocuments.student_id == student_id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Academic documents record already exists")
    obj = models.AcademicDocuments(student_id=student_id, **data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/students/{student_id}/academic-documents", response_model=schemas.AcademicDocsResponse, tags=["Academic Documents"])
async def update_academic_docs(student_id: int, data: schemas.AcademicDocsCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.AcademicDocuments).where(models.AcademicDocuments.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Academic documents not found")
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/students/{student_id}/academic-documents", response_model=schemas.AcademicDocsResponse, tags=["Academic Documents"])
async def get_academic_docs(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.AcademicDocuments).where(models.AcademicDocuments.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Academic documents not found")
    return obj


@router.post("/students/{student_id}/academic-documents/upload", tags=["Academic Documents"])
async def upload_academic_docs(
    student_id: int,
    marksheets: Optional[UploadFile] = File(None),
    provisional_cert: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.AcademicDocuments).where(models.AcademicDocuments.student_id == student_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Academic documents record not found. Create it first.")
    if marksheets:
        obj.marksheets_path = save_file(student_id, marksheets)
    if provisional_cert:
        obj.provisional_cert_path = save_file(student_id, provisional_cert)
    await db.commit()
    return {"marksheets_path": obj.marksheets_path, "provisional_cert_path": obj.provisional_cert_path}


# ── Dashboard ─────────────────────────────────────────────────────────────────

@router.get("/dashboard/stats", response_model=schemas.DashboardStats, tags=["Dashboard"])
async def get_stats(db: AsyncSession = Depends(get_db)):
    total = (await db.execute(select(func.count()).select_from(models.Student))).scalar()

    hostellers = (await db.execute(
        select(func.count()).select_from(models.StudentClassification)
        .where(models.StudentClassification.is_hosteller == True)
    )).scalar()

    ncc_count = (await db.execute(
        select(func.count()).select_from(models.StudentClassification)
        .where(models.StudentClassification.ncc == True)
    )).scalar()

    nss_count = (await db.execute(
        select(func.count()).select_from(models.StudentClassification)
        .where(models.StudentClassification.nss == True)
    )).scalar()

    sports_count = (await db.execute(
        select(func.count()).select_from(models.StudentClassification)
        .where(models.StudentClassification.sports_quota == True)
    )).scalar()

    disabled_count = (await db.execute(
        select(func.count()).select_from(models.StudentClassification)
        .where(models.StudentClassification.is_disabled == True)
    )).scalar()

    # Category breakdown
    category_rows = (await db.execute(
        select(models.StudentClassification.category, func.count())
        .group_by(models.StudentClassification.category)
    )).all()
    category_breakdown = {str(row[0]): row[1] for row in category_rows}

    loan_count = (await db.execute(
        select(func.count()).select_from(models.FinancialInfo)
        .where(models.FinancialInfo.has_loan == True)
    )).scalar()

    scholarship_rows = (await db.execute(
        select(models.FinancialInfo.scholarship_type, func.count())
        .group_by(models.FinancialInfo.scholarship_type)
    )).all()
    scholarship_breakdown = {str(row[0]): row[1] for row in scholarship_rows}

    placed_count = (await db.execute(
        select(func.count()).select_from(models.Placement)
        .where(models.Placement.is_placed == True)
    )).scalar()

    higher_studies = (await db.execute(
        select(func.count()).select_from(models.Placement)
        .where(models.Placement.opted_higher_studies == True)
    )).scalar()

    entrepreneurship = (await db.execute(
        select(func.count()).select_from(models.Placement)
        .where(models.Placement.opted_entrepreneurship == True)
    )).scalar()

    internship_count = (await db.execute(select(func.count()).select_from(models.Internship))).scalar()
    research_count = (await db.execute(select(func.count()).select_from(models.ResearchPaper))).scalar()

    branch_rows = (await db.execute(
        select(models.Student.branch, func.count())
        .group_by(models.Student.branch)
    )).all()
    branch_wise = {row[0]: row[1] for row in branch_rows}

    year_rows = (await db.execute(
        select(models.Student.year, func.count())
        .group_by(models.Student.year)
    )).all()
    year_wise = {str(row[0]): row[1] for row in year_rows}

    return schemas.DashboardStats(
        total_students=total,
        hostellers=hostellers,
        day_scholars=total - hostellers,
        category_breakdown=category_breakdown,
        ncc_count=ncc_count,
        nss_count=nss_count,
        sports_quota_count=sports_count,
        disabled_count=disabled_count,
        loan_count=loan_count,
        scholarship_breakdown=scholarship_breakdown,
        placed_count=placed_count,
        higher_studies_count=higher_studies,
        entrepreneurship_count=entrepreneurship,
        internship_count=internship_count,
        research_count=research_count,
        branch_wise=branch_wise,
        year_wise=year_wise,
    )