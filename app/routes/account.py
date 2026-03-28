from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.authHelper import User, get_current_user, get_user_by_id
from app.services.account_services import changeUserPassword, resetPasswordToDefault
from app.core.database import get_db
from app.model.models import DBUser, RoleEnum

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


@router.post("/change-password")
async def change_password(
    new_password: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db)
):
    await changeUserPassword(db, current_user.id, new_password)
    return {"message": "password change successful"}


@router.post("/reset/{student_id}/password")
async def reset_password(
    student_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can reset passwords"
        )
    try:
        await resetPasswordToDefault(db, student_id)
        return {"message": f"Password reset to default for student {student_id}"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
