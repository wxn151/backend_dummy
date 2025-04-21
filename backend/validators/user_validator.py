from fastapi import HTTPException

def validate_email_domain(email: str):
    if not email.endswith("@example.com"):
        raise HTTPException(status_code=400, detail="Email must be @example.com")
