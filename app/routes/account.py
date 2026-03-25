from fastapi import APIRouter
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.services.authHelper import *

router = APIRouter(
    prefix="/account",
    tags=["account"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.post("/change/{user_id}/assword")
async def changePassword(user_id: int):
    return {"message": "to be implemented"}
