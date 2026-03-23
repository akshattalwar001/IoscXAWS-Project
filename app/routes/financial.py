from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db 
import app.schema.schemas as schemas 
from app.services import financial_services

router = APIRouter(
    prefix="/students/{student_id}/financial",
    tags=["Financial"]
)


@router.post("/", response_model=schemas.FinancialResponse)
async def create_financial(
    student_id: int,
    data: schemas.FinancialCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await financial_services.create_financial(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/", response_model=schemas.FinancialResponse)
async def update_financial(
    student_id: int,
    data: schemas.FinancialCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await financial_services.update_financial(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=schemas.FinancialResponse)
async def get_financial(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await financial_services.get_financial(db, student_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))