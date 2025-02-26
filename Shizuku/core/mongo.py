import logging

from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_DB_URI

meow = AsyncIOMotorClient(MONGO_DB_URI)
mongodb = meow.shizukumusic
logging.info("MongoDB Connected Successfully.")
