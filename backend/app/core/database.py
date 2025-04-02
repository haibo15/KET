from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

class Database:
    client: AsyncIOMotorClient = None
    
async def get_database() -> AsyncIOMotorClient:
    """
    获取数据库连接。
    """
    return Database.client[settings.DATABASE_NAME]

async def connect_to_mongo():
    """
    连接到MongoDB数据库。
    """
    Database.client = AsyncIOMotorClient(settings.MONGODB_URL)
    
async def close_mongo_connection():
    """
    关闭MongoDB连接。
    """
    if Database.client:
        Database.client.close() 