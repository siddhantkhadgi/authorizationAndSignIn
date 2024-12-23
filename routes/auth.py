from fastapi import APIRouter, HTTPException, Depends, Request
from models import User, InputTokenRequest
from utils import get_password_hash, verify_password, create_token, decode_token
from config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from datetime import timedelta, datetime
from db import get_database

auth_router = APIRouter()


@auth_router.post("/signup")
async def signup(user: User, db=Depends(get_database)):
    print(user)
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    await db["users"].insert_one({"email": user.email, "password": hashed_password})
    return {"message": "User registered successfully"}


@auth_router.post("/signin")
async def signin(user: User, db=Depends(get_database)):
    db_user = await db["users"].find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_token(
        {"sub": user.email}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        {"sub": user.email, "refresh": True},
        timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
    )

    await db["tokens"].insert_one({"token": refresh_token, "email": user.email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@auth_router.get("/authorize")
async def authorize(request: Request):
    token = request.headers.get("Authorization")
    print(token)
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token missing or invalid")

    token = token.split(" ")[1]
    print(token)
    payload = decode_token(token)
    print(payload)
    if not payload or payload.get("exp") < datetime.utcnow().timestamp():
        raise HTTPException(status_code=401, detail="Token expired or invalid")

    return {"message": "Token is valid", "user": payload["sub"]}
