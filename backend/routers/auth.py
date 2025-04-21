from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from pydantic import EmailStr
from backend.db.session import SessionLocal
from backend.db.models.user import User
from backend.schemas.user import UserCreate, UserLogin, TokenPayload
from backend.schemas.recover import EmailSchema, ResetPassword
from backend.utils.security import hash_password, verify_password
from backend.auth.jwt_handler import create, decode, create_one_time_use_token
from backend.auth.email import send_confirmation_mail, send_password_reset_link, GmailService
import hashlib

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def is_user_existing(db: Session, email: str, username: str) -> bool:
    existing = db.query(User).filter(
        or_(User.email == email, User.username == username)
    ).first()
    return existing is not None


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if is_user_existing(db, user.email, user.username):
        raise HTTPException(status_code=400, detail="Account already exist on db")

    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hash_password(user.password),
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_one_time_use_token(str(new_user.id))
    email_service = GmailService()
    send_confirmation_mail(new_user.email, token, email_service)

    return {"msg": "User pending to validation."}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if db_user.is_verified is False:
        raise HTTPException(status_code=401, detail="Account is not activated")

    token = create({
        "sub": str(db_user.id),
        "mail": db_user.email,
        "username": db_user.username,
        "role": db_user.role
    })
    return {"access_token": token, "token_type": "bearer"}


@router.post("/forgot-password")
async def forgot_password(data: EmailSchema, db: Session = Depends(get_db)):
    email = data.email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not valid token")

    token = create_one_time_use_token(str(user.id))
    email_service = GmailService()
    send_password_reset_link(user.email, token, email_service)

    return {"message": "Mail sent successfully."}


@router.post("/reset-password")
async def reset_password(data: ResetPassword, db: Session = Depends(get_db)):
    payload = decode(data.token, True)
    id = payload.get("sub")
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid token")
    hash = hash_password(data.new_password)
    if user.hashed_password == hash:
        raise HTTPException(status_code=404, detail="Must be a different password")
    user.hashed_password = hash
    db.commit()
    return {"message": "Password changed successfully."}


@router.post("/confirm-email")
async def confirm_email(data: TokenPayload, db: Session = Depends(get_db)):
    payload = decode(data.token, True)
    id = payload.get("sub")
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not valid token")
    if user.is_verified:
        return {"message": "The account is already verified."}
    user.is_verified = True
    db.commit()

    return {"message": "Account activated sucessfully."}


@router.post("/resend-confirmation")
def resend_confirmation(email: EmailStr, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    if user.is_verified:
        return {"message": "The account is already verified."}

    token = create_one_time_use_token(str(user.id))
    email_service = GmailService()
    send_confirmation_mail(user.email, token, email_service)

    return {"message": "Mail sent successfully."}