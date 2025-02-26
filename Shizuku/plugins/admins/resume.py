from pyrogram import filters
from pyrogram.types import Message

from Shizuku import app
from Shizuku.core.call import ShizukuMusic
from Shizuku.utils.database import is_music_playing, music_on
from Shizuku.utils.decorators import AdminRightsCheck
from Shizuku.utils.inline import close_markup


@app.on_message(filters.command(["resume", "cresume"]) & filters.group)
@AdminRightsCheck
async def resume_com(cli, message: Message, chat_id):
    if await is_music_playing(chat_id):
        return await message.reply_text("Stream is already resumed.")
    await music_on(chat_id)
    await ShizukuMusic.resume_stream(chat_id)
    await message.reply_text(
        "Stream resumed by {}".format(message.from_user.mention),
        reply_markup=close_markup(),
    )
