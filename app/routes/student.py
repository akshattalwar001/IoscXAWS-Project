from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
import app.schema.schemas as schemas

from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.services import student_services


router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=schemas.StudentResponse)
async def create_student(student: schemas.StudentCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await student_services.create_student(db, student)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[schemas.StudentResponse])
async def list_students(
    branch: Optional[str] = None,
    year: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await student_services.list_students(db, branch, year)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{student_id}", response_model=schemas.FullStudentProfile)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await student_services.get_student_full(db, student_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{student_id}", response_model=schemas.StudentResponse)
async def update_student(student_id: int, data: schemas.StudentUpdate, db: AsyncSession = Depends(get_db)):
    try:
        return await student_services.update_student(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{student_id}")
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await student_services.delete_student(db, student_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{student_id}/photo")
async def upload_photo(student_id: int, photo: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    try:
        return await student_services.upload_photo(db, student_id, photo)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{student_id}/signature")
async def upload_signature(student_id: int, signature: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    try:
        return await student_services.upload_signature(db, student_id, signature)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))