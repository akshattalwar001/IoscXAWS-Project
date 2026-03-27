from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import app.schema.schemas as schemas
from app.services import academic_services
from app.core.database import get_db
from app.services.authorization_services import verify_user_access

router = APIRouter(
    prefix="/students/{student_id}/academic",
    tags=["Academic"],
    dependencies=[Depends(verify_user_access)]
)


@router.post("/", response_model=schemas.AcademicResponse)
async def create_academic(
    student_id: str,
    data: schemas.AcademicCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await academic_services.create_academic(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/", response_model=schemas.AcademicResponse)
async def update_academic(
    student_id: str,
    data: schemas.AcademicCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await academic_services.update_academic(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=schemas.AcademicResponse)
async def get_academic(
    student_id: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await academic_services.get_academic(db, student_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
