from fastapi import APIRouter, HTTPException, Depends
from utils import decode_token, create_token
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from models import InputTokenRequest
from db import get_database

token_router = APIRouter()


@token_router.post("/revoke")
async def revoke_token(request: InputTokenRequest, db=Depends(get_database)):
    deleted = await db["tokens"].delete_one({"token": request.token})
    if deleted.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Token not found")
    return {"message": "Token revoked successfully"}


@token_router.post("/refresh")
async def refresh_token(request: InputTokenRequest, db=Depends(get_database)):
    payload = decode_token(request.token)
    if not payload or not payload.get("refresh"):
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    db_token = await db["tokens"].find_one({"token": request.token})
    if not db_token:
        raise HTTPException(status_code=404, detail="Token not found")

    new_access_token = create_token(
        {"sub": payload["sub"]}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": new_access_token, "token_type": "bearer"}
