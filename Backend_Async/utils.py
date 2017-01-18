import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


async def initdb():
    client = AsyncIOMotorClient('mongodb://172.17.0.2:27017')
    db = client.backend_log
    return db
