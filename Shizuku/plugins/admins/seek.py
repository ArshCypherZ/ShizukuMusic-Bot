from pyrogram import filters
from pyrogram.types import Message

import logging

from Shizuku import YouTube, app
from Shizuku.core.call import ShizukuMusic
from Shizuku.misc import db
from Shizuku.utils import AdminRightsCheck, seconds_to_min
from Shizuku.utils.inline import close_markup


@app.on_message(
    filters.command(["seek", "cseek", "seekback", "cseekback"]) & filters.group
)
@AdminRightsCheck
async def seek_comm(cli, message: Message, chat_id):
    if len(message.command) == 1:
        return await message.reply_text(
            "Example: /seek or /seekback [duration in seconds]"
        )
    query = message.text.split(None, 1)[1].strip()
    if not query.isnumeric():
        return await message.reply_text("Please use numeric digits to seek.")
    playing = db.get(chat_id)
    if not playing:
        return await message.reply_text("Queue is empty.")
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await message.reply_text("Live streams cannot be seeked.")
    file_path = playing[0]["file"]
    duration_played = int(playing[0]["played"])
    duration_to_skip = int(query)
    duration = playing[0]["dur"]
    if message.command[0][-2] == "c":
        if (duration_played - duration_to_skip) <= 10:
            return await message.reply_text(
                text="Try seeking with lower duration. Played {} out of {} minutes.".format(
                    seconds_to_min(duration_played), duration
                ),
                reply_markup=close_markup(),
            )
        to_seek = duration_played - duration_to_skip + 1
    else:
        if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
            return await message.reply_text(
                text="Try seeking with lower duration. Played {} out of {} minutes.".format(
                    seconds_to_min(duration_played), duration
                ),
                reply_markup=close_markup(),
            )
        to_seek = duration_played + duration_to_skip + 1
    mystic = await message.reply_text("Seeking. Please wait.")
    if "vid_" in file_path:
        n, file_path = await YouTube.video(playing[0]["vidid"], True)
        if n == 0:
            return await message.reply_text("Live streams cannot be seeked.")
    check = (playing[0]).get("speed_path")
    if check:
        file_path = check
    if "index_" in file_path:
        file_path = playing[0]["vidid"]
    try:
        await ShizukuMusic.seek_stream(
            chat_id,
            file_path,
            seconds_to_min(to_seek),
            duration,
            playing[0]["streamtype"],
        )
    except Exception as e:
        logging.error(e)
        return await mystic.edit_text("Failed to seek.", reply_markup=close_markup())
    if message.command[0][-2] == "c":
        db[chat_id][0]["played"] -= duration_to_skip
    else:
        db[chat_id][0]["played"] += duration_to_skip
    await mystic.edit_text(
        text="Stream successfully seeked. Duration {} by {}".format(
            seconds_to_min(to_seek), message.from_user.mention
        ),
        reply_markup=close_markup(),
    )
