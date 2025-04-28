# backend/routers/user.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.db.models.user import User
from backend.schemas.user import UserOut, ToggleActive
from backend.dependencies.auth import get_current_user

# DEFAULT PREFIX
router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Devuelve la información del usuario (loggueado).

    **Respuesta**
    - Datos del usuario actual
    """
    return current_user

@router.put("/toggle", response_model=UserOut)
def toggle_user_active(
    toggle: ToggleActive,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Dar de baja o alta a un usuario.
    **Parámetros**
    - `is_active`: estado actual de la cuenta

    **Respuesta**
    - Datos del usuario actualizado
    """

    current_user.is_active = toggle.is_active
    db.commit()
    db.refresh(current_user)
    return current_user
    