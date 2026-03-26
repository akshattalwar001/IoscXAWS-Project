from fastapi import APIRouter
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.services.authHelper import *
from app.services.account_services import *

router = APIRouter(
    prefix="/account",
    tags=["account"],
    responses={404: {"description": "Not found"}},
)
@router.get("/whoami") 
async def whoAmI(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return {"message": f"you are {current_user.username} with id {current_user.id} "}

@router.post("/change/{user_id}/password") 
async def change_password(
    user_id: int,
    new_password: str,
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only change your own password"
        )

    await changeUserPassword(user_id,new_password)
    return {"message": f" password change successfull "}
