from pyrogram import filters
from pyrogram.types import Message

from Shizuku import app
from Shizuku.core.call import ShizukuMusic
from Shizuku.utils.database import set_loop
from Shizuku.utils.decorators import AdminRightsCheck
from Shizuku.utils.inline import close_markup


@app.on_message(filters.command(["end", "stop", "cend", "cstop"]) & filters.group)
@AdminRightsCheck
async def stop_music(cli, message: Message, chat_id):
    if not len(message.command) == 1:
        return
    await ShizukuMusic.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(
        "Stream stopped by {}".format(message.from_user.mention),
        reply_markup=close_markup(),
    )
