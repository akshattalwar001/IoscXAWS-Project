from fastapi import Path, HTTPException, status, Depends

from app.services.authHelper import DBUser, get_current_user, RoleEnum

async def verify_user_access(
    student_id: str = Path(...), 
    current_user: DBUser = Depends(get_current_user),
):
    if str(current_user.role) == RoleEnum.admin:
        return current_user
        
    if str(current_user.role) == RoleEnum.student and student_id==current_user.username:
        return current_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to view or edit this student's data"
    )
