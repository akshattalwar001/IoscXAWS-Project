from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import app.schema.schemas as schemas
from app.core.database import get_db
from app.services import classification_services

router = APIRouter(
    prefix="/students/{student_id}/classification",
    tags=["Classification"]
)


@router.post("", response_model=schemas.ClassificationResponse)
async def create_classification(
    student_id: int,
    data: schemas.ClassificationCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await classification_services.create_classification(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/", response_model=schemas.ClassificationResponse)
async def update_classification(
    student_id: int,
    data: schemas.ClassificationCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await classification_services.update_classification(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=schemas.ClassificationResponse)
async def get_classification(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await classification_services.get_classification(db, student_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))