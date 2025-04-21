# schemas.py
from pydantic import BaseModel, EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: str

class EmailSchema(BaseModel):
    email: EmailStr
