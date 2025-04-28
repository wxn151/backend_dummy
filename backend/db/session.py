from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from backend.core.config import DATABASE_URL

# Create DB engine
engine = create_engine(DATABASE_URL)

# Create a configured session class
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Create base class for declarative models
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

