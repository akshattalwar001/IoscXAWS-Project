from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import app.schema.schemas as schemas
from app.core.database import get_db
from app.services import research_services


router = APIRouter(
    tags=["Research"]
)


@router.post("/students/{student_id}/research", response_model=schemas.ResearchResponse)
async def create_research(
    student_id: str,
    data: schemas.ResearchCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await research_services.create_research(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/students/{student_id}/research", response_model=List[schemas.ResearchResponse])
async def get_research(
    student_id: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await research_services.get_research(db, student_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/research/{paper_id}", response_model=schemas.ResearchResponse)
async def update_research(
    paper_id: int,
    data: schemas.ResearchCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await research_services.update_research(db, paper_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/research/{paper_id}")
async def delete_research(
    paper_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await research_services.delete_research(db, paper_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
