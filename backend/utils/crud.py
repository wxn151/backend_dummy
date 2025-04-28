from sqlalchemy.orm import Session
from backend.db.models.user import User
from sqlalchemy import or_


def is_user_existing(db: Session, email: str, username: str) -> bool:
    existing = db.query(User).filter(
        or_(User.email == email, User.username == username)
    ).first()
    return existing is not None