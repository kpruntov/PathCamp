# @trace TASK-011
# @trace TASK-012
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.dependencies import get_db, get_current_user
from app.models import User

router = APIRouter(prefix="/admin/users", tags=["admin"])

@router.get("", response_model=schemas.UserListResponse)
def get_user_list(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # In a real app, check if current_user has Admin role
    users = crud.get_users(db)
    return schemas.UserListResponse(users=users)

@router.put("/{userId}/status", response_model=schemas.UserStatusResponse)
def update_user_status(
    userId: int, 
    status_update: schemas.UserStatusUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Check Admin role
    updated_user = crud.update_user_status(db, user_id=userId, status=status_update.status)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return schemas.UserStatusResponse(user_id=str(updated_user.id), status=updated_user.status)
