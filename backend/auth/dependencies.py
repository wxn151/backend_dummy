from fastapi import Depends, HTTPException
from backend.auth.jwt_handler import current_jwt

def require_role(role: str):
    def role_checker(current_user: dict = Depends(current_jwt)):
        if current_user["role"] != role:
            raise HTTPException(status_code=403, detail="No autorizado")
        return current_user
    return role_checker
