import logging

from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, BOT_ID, BOT_USERNAME, BOT_NAME


class ShizukuMusic(Client):
    def __init__(self):
        logging.info("Starting Bot.")
        super().__init__(
            name=BOT_NAME,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            in_memory=True,
            sleep_threshold=0,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = BOT_ID
        self.name = BOT_NAME
        self.username = BOT_USERNAME
        self.mention = f"[{self.name}](tg://user?id={self.id})"

        logging.info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
