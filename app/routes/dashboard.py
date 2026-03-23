from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import app.schema.schemas as schemas

from app.core.database import get_db
from app.services import dashboard_services


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats", response_model=schemas.DashboardStats)
async def get_stats(db: AsyncSession = Depends(get_db)):
    try:
        return await dashboard_services.get_dashboard_stats(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))