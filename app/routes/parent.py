from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services import parent_services
import app.schema.schemas as schemas


router = APIRouter(
    prefix="/students/{student_id}/parent",
    tags=["Parent"]
)


@router.post("/", response_model=schemas.ParentResponse)
async def create_parent(
    student_id: int,
    data: schemas.ParentCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await parent_services.create_parent(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/", response_model=schemas.ParentResponse)
async def update_parent(
    student_id: int,
    data: schemas.ParentCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await parent_services.update_parent(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=schemas.ParentResponse)
async def get_parent(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await parent_services.get_parent(db, student_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))