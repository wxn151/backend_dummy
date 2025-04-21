from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from backend.core.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# create JWT
def create(data: dict, expires_delta: timedelta = timedelta(minutes=20)):
    # ACCESS_TOKEN_EXPIRE_MINUTES
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# decode JWT
def decode(token: str, otu: bool = False):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        if otu:
            if payload.get("type") != "OTU":
                raise HTTPException(status_code=400, detail="Ups, not valid token.")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail=f"Invalid token or expired")

def current_jwt(token: str = Depends(oauth2_scheme)):
    payload = decode(token)
    return payload

def create_one_time_use_token(id: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=48)
    payload = {"sub": id, "type": "OTU", "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
