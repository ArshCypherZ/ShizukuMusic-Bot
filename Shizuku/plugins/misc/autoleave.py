import asyncio
from datetime import datetime

from pyrogram.enums import ChatType

import config
from Shizuku import app
from Shizuku.core.call import ShizukuMusic, autoend
from Shizuku.utils.database import get_client, is_active_chat, is_autoend


async def auto_leave():
    if config.AUTO_LEAVING_ASSISTANT:
        while not await asyncio.sleep(900):
            from Shizuku.core.userbot import assistants

            for num in assistants:
                client = await get_client(num)
                left = 0
                try:
                    async for i in client.get_dialogs():
                        if i.chat.type in [
                            ChatType.SUPERGROUP,
                            ChatType.GROUP,
                            ChatType.CHANNEL,
                        ]:
                            if i.chat.id != config.LOGGER_ID:
                                if left == 20:
                                    continue
                                if not await is_active_chat(i.chat.id):
                                    try:
                                        await client.leave_chat(i.chat.id)
                                        left += 1
                                    except BaseException:
                                        continue
                except BaseException:
                    pass


asyncio.create_task(auto_leave())


async def auto_end():
    while not await asyncio.sleep(5):
        ender = await is_autoend()
        if not ender:
            continue
        for chat_id in autoend:
            timer = autoend.get(chat_id)
            if not timer:
                continue
            if datetime.now() > timer:
                if not await is_active_chat(chat_id):
                    autoend[chat_id] = {}
                    continue
                autoend[chat_id] = {}
                try:
                    await ShizukuMusic.stop_stream(chat_id)
                except BaseException:
                    continue
                try:
                    await app.send_message(
                        chat_id,
                        "Bot left vc because no one was listening.",
                    )
                except BaseException:
                    continue


asyncio.create_task(auto_end())
