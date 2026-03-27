from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

import app.schema.schemas as schemas
from app.core.database import get_db
from app.services import document_services
from app.services.authorization_services import verify_user_access


router = APIRouter(
    prefix="/students/{student_id}/documents",
    tags=["Documents"],
    dependencies=[Depends(verify_user_access)]
)


@router.post("/", response_model=schemas.DocumentsResponse)
async def create_documents(
    student_id: str,
    data: schemas.DocumentsCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await document_services.create_documents(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/", response_model=schemas.DocumentsResponse)
async def update_documents(
    student_id: str,
    data: schemas.DocumentsCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await document_services.update_documents(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=schemas.DocumentsResponse)
async def get_documents(
    student_id: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await document_services.get_documents(db, student_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/upload")
async def upload_documents(
    student_id: str,
    aadhaar: Optional[UploadFile] = File(None),
    pan: Optional[UploadFile] = File(None),
    id_card: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    try:
        return await document_services.upload_documents(
            db,
            student_id,
            aadhaar,
            pan,
            id_card
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
