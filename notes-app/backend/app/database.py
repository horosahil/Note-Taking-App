from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "notes_app")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "changeme")
    JWT_EXPIRES_MINUTES: int = int(os.getenv("JWT_EXPIRES_MINUTES", "120"))
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:3000")

settings = Settings()

client: Optional[AsyncIOMotorClient] = None
db = None

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]

async def close_mongo_connection():
    global client
    if client:
        client.close()