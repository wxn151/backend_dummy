from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=4, max_length=30)
    password: str = Field(min_length=8, max_length=100)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

### schema USER

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: Optional[str]
    is_verified: bool
    # is_active: bool   # <= hidden for obvious porpuses
    role: str

    class Config:
        orm_mode = True

class ToggleActive(BaseModel):
    is_active: bool

class TokenPayload(BaseModel):
    token: str

## schema ADMIN




