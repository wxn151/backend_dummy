from fastapi import APIRouter, Depends
from backend.auth.dependencies import require_role

router = APIRouter()

@router.get("/admin-only")
def admin_endpoint(user=Depends(require_role("admin"))):
    return {"message": "ADMIN privileges"}
