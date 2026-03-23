from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

import app.schema.schemas as schemas
from app.core.database import get_db
from app.services import academic_document_services


router = APIRouter(
    prefix="/students/{student_id}/academic-documents",
    tags=["Academic Documents"]
)


@router.post("/", response_model=schemas.AcademicDocsResponse)
async def create_academic_docs(
    student_id: int,
    data: schemas.AcademicDocsCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await academic_document_services.create_academic_docs(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/", response_model=schemas.AcademicDocsResponse)
async def update_academic_docs(
    student_id: int,
    data: schemas.AcademicDocsCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await academic_document_services.update_academic_docs(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=schemas.AcademicDocsResponse)
async def get_academic_docs(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await academic_document_services.get_academic_docs(db, student_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/upload")
async def upload_academic_docs(
    student_id: int,
    marksheets: Optional[UploadFile] = File(None),
    provisional_cert: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    try:
        return await academic_document_services.upload_academic_docs(
            db,
            student_id,
            marksheets,
            provisional_cert
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))