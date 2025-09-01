from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

def create_jwt(subject: str, secret: str, expires_minutes: int) -> str:
    now = datetime.utcnow()
    payload = {"sub": subject, "iat": now, "exp": now + timedelta(minutes=expires_minutes)}
    return jwt.encode(payload, secret, algorithm="HS256")

def decode_jwt(token: str, secret: str) -> Optional[dict]:
    try:
        return jwt.decode(token, secret, algorithms=["HS256"])
    except Exception:
        return None