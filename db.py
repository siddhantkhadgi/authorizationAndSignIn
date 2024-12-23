from config import MONGO_URL, DATABASE_NAME
from motor.motor_asyncio import AsyncIOMotorClient

db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client[DATABASE_NAME]


def get_database():
    return db


def shutdown_db_client():
    db_client.close()
