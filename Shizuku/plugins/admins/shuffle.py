import random

from pyrogram import filters
from pyrogram.types import Message

from Shizuku import app
from Shizuku.misc import db
from Shizuku.utils.decorators import AdminRightsCheck
from Shizuku.utils.inline import close_markup


@app.on_message(filters.command(["shuffle", "cshuffle"]) & filters.group)
@AdminRightsCheck
async def admins(Client, message: Message, chat_id):
    check = db.get(chat_id)
    if not check:
        return await message.reply_text("Queue is empty.")
    try:
        popped = check.pop(0)
    except BaseException:
        return await message.reply_text(
            "Failed to shuffle, check queue by /queue", reply_markup=close_markup()
        )
    check = db.get(chat_id)
    if not check:
        check.insert(0, popped)
        return await message.reply_text(
            "Failed to shuffle, check queue by /queue", reply_markup=close_markup()
        )
    random.shuffle(check)
    check.insert(0, popped)
    await message.reply_text(
        "Queue shuffled by {}. Check it by /queue".format(message.from_user.mention),
        reply_markup=close_markup(),
    )
