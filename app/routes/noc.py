from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import app.schema.schemas as schemas
from app.core.database import get_db
from app.services import noc_services
from app.services.authorization_services import verify_user_access


router = APIRouter(
    prefix="/students/{student_id}/noc",
    tags=["NOC"],
    dependencies=[Depends(verify_user_access)]
)


@router.post("/", response_model=schemas.NocResponse)
async def create_noc(
    student_id: str,
    data: schemas.NocCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await noc_services.create_noc(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/", response_model=schemas.NocResponse)
async def update_noc(
    student_id: str,
    data: schemas.NocCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await noc_services.update_noc(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=schemas.NocResponse)
async def get_noc(
    student_id: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await noc_services.get_noc(db, student_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
