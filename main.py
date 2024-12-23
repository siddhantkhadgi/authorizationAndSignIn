from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from routes.auth import auth_router
from routes.token import token_router
from config import MONGO_URL, DATABASE_NAME
from db import get_database, shutdown_db_client

app = FastAPI()

# Include Routers
app.include_router(auth_router, prefix="/auth")
app.include_router(token_router, prefix="/token")

get_database()


@app.on_event("shutdown")
async def shutdown_db_client():
    shutdown_db_client()
