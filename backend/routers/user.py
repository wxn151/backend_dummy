# backend/routers/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.db.models.user import User
from backend.schemas.user import UserOut, UpdatePassword, ToggleActive
from backend.utils.security import verify_password, hash_password
from backend.utils.auth import get_current_user

# DEFAULT PREFIX
router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/password")
def reset_password(
    data: UpdatePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")

    current_user.hashed_password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}


@router.put("/toggle", response_model=UserOut)
def toggle_user_active(
    toggle: ToggleActive,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.is_active = toggle.is_active
    db.commit()
    db.refresh(current_user)
    return current_user
