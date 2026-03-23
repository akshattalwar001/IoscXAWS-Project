from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import app.schema.schemas as schemas
from app.core.database import get_db
from app.services import placement_services


router = APIRouter(
    prefix="/students/{student_id}/placement",
    tags=["Placement"]
)


@router.post("/", response_model=schemas.PlacementResponse)
async def create_placement(
    student_id: int,
    data: schemas.PlacementCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await placement_services.create_placement(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/", response_model=schemas.PlacementResponse)
async def update_placement(
    student_id: int,
    data: schemas.PlacementCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await placement_services.update_placement(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=schemas.PlacementResponse)
async def get_placement(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await placement_services.get_placement(db, student_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))