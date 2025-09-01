from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi import Request
from pydantic import EmailStr
from .database import db, settings
from .models import UserDB
from .schemas import UserCreate, UserLogin, UserPublic
from .utils import hash_password, verify_password, create_jwt, decode_jwt

router = APIRouter(prefix="/api/auth", tags=["auth"])

COOKIE_NAME = "access_token"

@router.post("/register", response_model=UserPublic, status_code=201)
async def register(payload: UserCreate):
    existing = await db.users.find_one({"user_email": payload.user_email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = UserDB(
        user_name=payload.user_name,
        user_email=payload.user_email,
        password_hash=hash_password(payload.password),
    )
    await db.users.insert_one(user.model_dump())
    return UserPublic(
        user_id=user.user_id,
        user_name=user.user_name,
        user_email=user.user_email,
        created_on=user.created_on,
        last_update=user.last_update,
    )

@router.post("/login", response_model=UserPublic)
async def login(payload: UserLogin, response: Response):
    doc = await db.users.find_one({"user_email": payload.user_email})
    if not doc:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user = UserDB(**doc)
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt(user.user_id, settings.JWT_SECRET, settings.JWT_EXPIRES_MINUTES)
    # HttpOnly cookie
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=settings.JWT_EXPIRES_MINUTES * 60,
        path="/",
    )
    return UserPublic(
        user_id=user.user_id,
        user_name=user.user_name,
        user_email=user.user_email,
        created_on=user.created_on,
        last_update=user.last_update,
    )

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(COOKIE_NAME, path="/")
    return {"ok": True}

@router.get("/me", response_model=UserPublic)
async def me(request: Request):
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    data = decode_jwt(token, settings.JWT_SECRET)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = data.get("sub")
    doc = await db.users.find_one({"user_id": user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="User not found")
    user = UserDB(**doc)
    return UserPublic(
        user_id=user.user_id,
        user_name=user.user_name,
        user_email=user.user_email,
        created_on=user.created_on,
        last_update=user.last_update,
    )