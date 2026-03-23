from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import app.schema.schemas as schemas
from app.core.database import get_db
from app.services import internship_services


router = APIRouter(
    tags=["Internships"]
)


@router.post("/students/{student_id}/internships", response_model=schemas.InternshipResponse)
async def create_internship(
    student_id: int,
    data: schemas.InternshipCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await internship_services.create_internship(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/students/{student_id}/internships", response_model=List[schemas.InternshipResponse])
async def get_internships(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await internship_services.get_internships(db, student_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/internships/{internship_id}", response_model=schemas.InternshipResponse)
async def update_internship(
    internship_id: int,
    data: schemas.InternshipCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await internship_services.update_internship(db, internship_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/internships/{internship_id}")
async def delete_internship(
    internship_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await internship_services.delete_internship(db, internship_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))