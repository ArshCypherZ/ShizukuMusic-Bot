from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message

import config
from Shizuku import YouTube, app
from Shizuku.core.call import ShizukuMusic
from Shizuku.misc import db
from Shizuku.utils.database import get_loop
from Shizuku.utils.decorators import AdminRightsCheck
from Shizuku.utils.inline import close_markup, stream_markup
from Shizuku.utils.stream.autoclear import auto_clean


@app.on_message(filters.command(["skip", "cskip", "next", "cnext"]) & filters.group)
@AdminRightsCheck
async def skip(cli, message: Message, chat_id):
    if not len(message.command) < 2:
        loop = await get_loop(chat_id)
        if loop != 0:
            return await message.reply_text(
                "Please try to disable loop play by /loop disable and then try again to skip."
            )
        state = message.text.split(None, 1)[1].strip()
        if state.isnumeric():
            state = int(state)
            check = db.get(chat_id)
            if check:
                count = len(check)
                if count > 2:
                    count = int(count - 1)
                    if 1 <= state <= count:
                        for x in range(state):
                            popped = None
                            try:
                                popped = check.pop(0)
                            except BaseException:
                                return await message.reply_text(
                                    "Failed to skip the requested track. Check /queue"
                                )
                            if popped:
                                await auto_clean(popped)
                            if not check:
                                try:
                                    await message.reply_text(
                                        text="Stream skipped by {} in {}".format(
                                            message.from_user.mention,
                                            message.chat.title,
                                        ),
                                        reply_markup=close_markup(),
                                    )
                                    await ShizukuMusic.stop_stream(chat_id)
                                except BaseException:
                                    return
                                break
                    else:
                        return await message.reply_text(
                            "Not enough tracks in queue to skip. Skip in between 1 and {}".format(
                                count
                            )
                        )
                else:
                    return await message.reply_text(
                        "Atleast 2 tracks needed in queue to skip."
                    )
            else:
                return await message.reply_text("Queue is empty.")
        else:
            return await message.reply_text(
                "Please use specific number to skip the track. Like 1, 2, 3"
            )
    else:
        check = db.get(chat_id)
        popped = None
        try:
            popped = check.pop(0)
            if popped:
                await auto_clean(popped)
            if not check:
                await message.reply_text(
                    text="Stream skipped by {} in {}".format(
                        message.from_user.mention, message.chat.title
                    ),
                    reply_markup=close_markup(),
                )
                try:
                    return await ShizukuMusic.stop_stream(chat_id)
                except BaseException:
                    return
        except BaseException:
            try:
                await message.reply_text(
                    text="Stream skipped by {} in {}".format(
                        message.from_user.mention, message.chat.title
                    ),
                    reply_markup=close_markup(),
                )
                return await ShizukuMusic.stop_stream(chat_id)
            except BaseException:
                return
    queued = check[0]["file"]
    title = (check[0]["title"]).title()
    user = check[0]["by"]
    streamtype = check[0]["streamtype"]
    videoid = check[0]["vidid"]
    status = True if str(streamtype) == "video" else None
    db[chat_id][0]["played"] = 0
    exis = (check[0]).get("old_dur")
    if exis:
        db[chat_id][0]["dur"] = exis
        db[chat_id][0]["seconds"] = check[0]["old_second"]
        db[chat_id][0]["speed_path"] = None
        db[chat_id][0]["speed"] = 1.0
    if "live_" in queued:
        n, link = await YouTube.video(videoid, True)
        if n == 0:
            return await message.reply_text(
                "Error while changing stream to {}".format(title)
            )
        try:
            await ShizukuMusic.skip_stream(chat_id, link, video=status)
        except BaseException:
            return await message.reply_text("Failed to switch stream, do /skip again.")
        button = stream_markup(chat_id)
        k = "<b>Started Streaming</b>\n\n<b>Title:</b> <a href={}>{}</a>\n<b>Duration:</b> {} minutes\n<b>Requested by:</b> {}"
        run = await message.reply_text(
            text=k.format(
                f"https://t.me/{app.username}?start=info_{videoid}",
                title[:30],
                check[0]["dur"],
                user,
            ),
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "tg"
    elif "vid_" in queued:
        mystic = await message.reply_text(
            "Downloading next track..Please wait.", disable_web_page_preview=True
        )
        try:
            file_path, direct = await YouTube.download(
                videoid,
                mystic,
                videoid=True,
                video=status,
            )
        except BaseException:
            return await mystic.edit_text("Failed to switch streams, try /skip again.")
        try:
            await ShizukuMusic.skip_stream(chat_id, file_path, video=status)
        except BaseException:
            return await mystic.edit_text("Failed to switch streams, try /skip again.")
        button = stream_markup(chat_id)
        ke = "<b>Started Streaming</b>\n\n<b>Title:</b> <a href={}>{}</a>\n<b>Duration:</b> {} minutes\n<b>Requested by:</b> {}"
        run = await message.reply_text(
            text=ke.format(
                f"https://t.me/{app.username}?start=info_{videoid}",
                title[:30],
                check[0]["dur"],
                user,
            ),
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "stream"
        await mystic.delete()
    elif "index_" in queued:
        try:
            await ShizukuMusic.skip_stream(chat_id, videoid, video=status)
        except BaseException:
            return await message.reply_text("Failed to switch stream. Try /skip again.")
        button = stream_markup(chat_id)
        x = "<b>Started Streaming</b>\n\n<b>Stream Type:</b> Live Stream [URL]\n<b>Requested by:</b> {}"
        run = await message.reply_text(
            text=x.format(user),
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "tg"
    else:
        try:
            await ShizukuMusic.skip_stream(chat_id, queued, video=status)
        except BaseException:
            return await message.reply_text("Failed to switch stream. Try /skip again.")
        if videoid == "telegram":
            button = stream_markup(chat_id)
            x = "<b>Started Streaming</b>\n\n<b>Title:</b> <a href={}>{}</a>\n<b>Duration:</b> {} minutes\n<b>Requested by:</b> {}"
            run = await message.reply_text(
                text=x.format(config.SUPPORT_CHAT, title[:30], check[0]["dur"], user),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        elif videoid == "soundcloud":
            button = stream_markup(chat_id)
            x = "<b>Started Streaming</b>\n\n<b>Title:</b> <a href={}>{}</a>\n<b>Duration:</b> {} minutes\n<b>Requested by:</b> {}"
            run = await message.reply_text(
                text=x.format(config.SUPPORT_CHAT, title[:30], check[0]["dur"], user),
                reply_markup=InlineKeyboardMarkup(button),
                disable_web_page_preview=True
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        else:
            button = stream_markup(chat_id)
            x = "<b>Started Streaming</b>\n\n<b>Title:</b> <a href={}>{}</a>\n<b>Duration:</b> {} minutes\n<b>Requested by:</b> {}"
            run = await message.reply_text(
                text=x.format(
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    title[:30],
                    check[0]["dur"],
                    user,
                ),
                reply_markup=InlineKeyboardMarkup(button),
                disable_web_page_preview=True
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
