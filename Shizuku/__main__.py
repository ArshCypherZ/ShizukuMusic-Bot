import asyncio
import importlib
import logging

from pyrogram import idle

from Shizuku import app, userbot
from Shizuku.backup import send
from Shizuku.core.call import ShizukuMusic
from Shizuku.plugins import ALL_MODULES

loop = asyncio.get_event_loop_policy().get_event_loop()


async def init():
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("Shizuku.plugins" + all_module)
    logging.info("Successfully imported all modules.")
    await send()
    await userbot.start()
    await ShizukuMusic.start()
    await ShizukuMusic.decorators()
    await idle()
    await app.stop()
    await userbot.stop()
    logging.info("Successfully stopped Shizuku.")


if __name__ == "__main__":
    loop.run_until_complete(init())
