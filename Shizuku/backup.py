import logging as LOGGER

from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_DB_URI, LOGGER_ID as CHANNEL_ID, BOT_NAME

meow = AsyncIOMotorClient(MONGO_DB_URI)
db = meow.shizukumusic
LOGGER.info("MongoDB Connected Successfully.")

import os
import asyncio
import bson
import shutil
from datetime import datetime
from Shizuku import app


async def dump():
    if not os.path.isdir("backup"):
        os.mkdir("backup")
    path = os.path.join(os.getcwd(), "backup")
    for coll in await db.list_collection_names():
        LOGGER.error(f"Dumping collection: {coll}")
        collection = db[coll]
        file_path = os.path.join(path, f'{coll}.bson')
        with open(file_path, 'ab') as f:
            async for doc in collection.find():
                f.write(bson.BSON.encode(doc))
        LOGGER.error(f"Dumped collection to {file_path}")

async def send():
    await dump()
    backup_dir = "backup"
    if os.path.isdir(backup_dir):
        LOGGER.error(f"Contents of {backup_dir}: {os.listdir(backup_dir)}")
    else:
        LOGGER.error(f"{backup_dir} directory does not exist")

    process = await asyncio.create_subprocess_shell("zip -r backup.zip backup", shell=True, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        LOGGER.error(f"ZIP process failed with error code {process.returncode}")
        if stdout:
            LOGGER.error(f"STDOUT: {stdout.decode()}")
        if stderr:
            LOGGER.error(f"STDERR: {stderr.decode()}")
        return
    if not os.path.isfile("backup.zip"):
        LOGGER.error("Backup file 'backup.zip' does not exist.")
        return
    if os.path.getsize("backup.zip") == 0:
        LOGGER.error("Backup file 'backup.zip' is empty.")
        return
    try:
        await app.send_document(CHANNEL_ID, "backup.zip", caption="**{} MongoDB Backup**\n**Date**: `{}`".format(BOT_NAME, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
    except Exception as e:
        LOGGER.error(f"Failed to send backup file: {e}")

    try:
        os.remove("backup.zip")
    except Exception as e:
        LOGGER.error(f"Failed to remove backup.zip: {e}")
    try:
        shutil.rmtree("backup")
    except Exception as e:
        LOGGER.error(f"Failed to remove backup directory: {e}")
