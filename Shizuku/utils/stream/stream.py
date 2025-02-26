import os
from typing import Union
import logging

from pyrogram.types import InlineKeyboardMarkup

import config
from Shizuku import YouTube, app
from Shizuku.core.call import ShizukuMusic
from Shizuku.misc import db
from Shizuku.utils.database import add_active_video_chat, is_active_chat
from Shizuku.utils.exceptions import AssistantErr
from Shizuku.utils.inline import aq_markup, close_markup, stream_markup
from Shizuku.utils.pastebin import paste
from Shizuku.utils.stream.queue import put_queue, put_queue_index


async def stream(
    mystic,
    user_id,
    result,
    chat_id,
    user_name,
    original_chat_id,
    video: Union[bool, str] = None,
    streamtype: Union[bool, str] = None,
    spotify: Union[bool, str] = None,
    forceplay: Union[bool, str] = None,
):
    if not result:
        return
    if forceplay:
        await ShizukuMusic.force_stop_stream(chat_id)
    if streamtype == "playlist":
        msg = "Queued Playlist:\n\n"
        count = 0
        for search in result:
            if int(count) == config.PLAYLIST_FETCH_LIMIT:
                continue
            try:
                (
                    title,
                    duration_min,
                    duration_sec,
                    vidid,
                ) = await YouTube.details(search, not spotify)
            except BaseException:
                continue
            if str(duration_min) == "None":
                continue
            if duration_sec > config.DURATION_LIMIT:
                continue
            if await is_active_chat(chat_id):
                check = db.get(chat_id)
                if len(check) > config.QUEUE_LIMIT:
                    return await app.send_message(
                        chat_id,
                        f"You are spamming. {config.QUEUE_LIMIT} songs in queue, either wait them to finish or use /end.",
                    )
                await put_queue(
                    chat_id,
                    original_chat_id,
                    f"vid_{vidid}",
                    title,
                    duration_min,
                    user_name,
                    vidid,
                    user_id,
                    "video" if video else "audio",
                )
                position = len(db.get(chat_id)) - 1
                count += 1
                msg += f"{count}. {title[:70]}\n"
                msg += f"Queued Position: {position}\n\n"
            else:
                if not forceplay:
                    db[chat_id] = []
                status = True if video else None
                try:
                    file_path, direct = await YouTube.download(
                        vidid, mystic, video=status, videoid=True
                    )
                except Exception as e:
                    logging.exception(e)
                    raise AssistantErr("Failed to fetch track details. Try any other.")
                await ShizukuMusic.join_call(
                    chat_id,
                    original_chat_id,
                    file_path,
                    video=status,
                )
                await put_queue(
                    chat_id,
                    original_chat_id,
                    file_path if direct else f"vid_{vidid}",
                    title,
                    duration_min,
                    user_name,
                    vidid,
                    user_id,
                    "video" if video else "audio",
                    forceplay=forceplay,
                )
                button = stream_markup(chat_id)
                meow = "<b> Started Streaming</b>\n\n<b>Title:</b> <a href={}>{}</a>\n<b>Duration:</b> {} minutes\n<b>Requested by:</b> {}"
                run = await app.send_message(
                    original_chat_id,
                    text=meow.format(
                        f"https://t.me/{app.username}?start=info_{vidid}",
                        title[:30],
                        duration_min,
                        user_name,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                    disable_web_page_preview=True
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"
        if count == 0:
            return
        link = await paste(msg)
        lines = msg.count("\n")
        car = os.linesep.join(msg.split(os.linesep)[:17]) if lines >= 17 else msg
        upl = close_markup()
        cv = "Added {} tracks to queue.\n\n<b>Check:</b> <a href={}>Click here</a>"
        return await app.send_message(
            original_chat_id,
            text=cv.format(position, link),
            reply_markup=upl,
        )
    elif streamtype == "youtube":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        duration_min = result["duration_min"]
        status = True if video else None
        try:
            file_path, direct = await YouTube.download(
                vidid, mystic, videoid=True, video=status
            )
        except Exception as e:
            logging.exception(e)
            raise AssistantErr("Failed to fetch track details. Try playing any other.")
        if await is_active_chat(chat_id):
            check = db.get(chat_id)
            if len(check) > config.QUEUE_LIMIT:
                return await app.send_message(
                    chat_id,
                    f"You are spamming. {config.QUEUE_LIMIT} songs in queue, either wait them to finish or use /end.",
                )
            await put_queue(
                chat_id,
                original_chat_id,
                file_path if direct else f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            button = aq_markup(chat_id)
            zn = "<b>Added to queue at #{}\n\nTitle:</b> {}\n<b>Duration:</b> {} minutes\n<b>Requested by:</b> {}"
            await app.send_message(
                chat_id=original_chat_id,
                text=zn.format(position, title[:27], duration_min, user_name),
                reply_markup=InlineKeyboardMarkup(button),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await ShizukuMusic.join_call(
                chat_id,
                original_chat_id,
                file_path,
                video=status,
            )
            await put_queue(
                chat_id,
                original_chat_id,
                file_path if direct else f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            button = stream_markup(chat_id)
            meo = "<b> Started Streaming</b>\n\n<b>Title:</b> <a href={}>{}</a>\n<b>Duration:</b> {} minutes\n<b>Requested by:</b> {}"
            run = await app.send_message(
                original_chat_id,
                text=meo.format(
                    f"https://t.me/{app.username}?start=info_{vidid}",
                    title[:30],
                    duration_min,
                    user_name,
                ),
                reply_markup=InlineKeyboardMarkup(button),
                disable_web_page_preview=True
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
    elif streamtype == "soundcloud":
        file_path = result["filepath"]
        title = result["title"]
        duration_min = result["duration_min"]
        if await is_active_chat(chat_id):
            check = db.get(chat_id)
            if len(check) > config.QUEUE_LIMIT:
                return await app.send_message(
                    chat_id,
                    f"You are spamming. {config.QUEUE_LIMIT} songs in queue, either wait them to finish or use /end.",
                )
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "audio",
            )
            position = len(db.get(chat_id)) - 1
            button = aq_markup(chat_id)
            mn = "<b>Added to queue at #{}\n\nTitle:</b> {}\n<b>Duration:</b> {} minutes\n<b>Requested by:</b> {}"
            await app.send_message(
                chat_id=original_chat_id,
                text=mn.format(position, title[:27], duration_min, user_name),
                reply_markup=InlineKeyboardMarkup(button),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await ShizukuMusic.join_call(
                chat_id, original_chat_id, file_path, video=None
            )
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "audio",
                forceplay=forceplay,
            )
            button = stream_markup(chat_id)
            me = "<b> Started Streaming</b>\n\n<b>Title:</b> <a href={}>{}</a>\n<b>Duration:</b> {} minutes\n<b>Requested by:</b> {}"
            run = await app.send_message(
                original_chat_id,
                text=me.format(
                    config.SUPPORT_CHAT, title[:30], duration_min, user_name
                ),
                reply_markup=InlineKeyboardMarkup(button),
                disable_web_page_preview=True
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
    elif streamtype == "telegram":
        file_path = result["path"]
        link = result["link"]
        title = (result["title"]).title()
        duration_min = result["dur"]
        status = True if video else None
        if await is_active_chat(chat_id):
            check = db.get(chat_id)
            if len(check) > config.QUEUE_LIMIT:
                return await app.send_message(
                    chat_id,
                    f"You are spamming. {config.QUEUE_LIMIT} songs in queue, either wait them to finish or use /end.",
                )
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            button = aq_markup(chat_id)
            m = "<b>Added to queue at #{}\n\nTitle:</b> {}\n<b>Duration:</b> {} minutes\n<b>Requested by:</b> {}"
            await app.send_message(
                chat_id=original_chat_id,
                text=m.format(position, title[:27], duration_min, user_name),
                reply_markup=InlineKeyboardMarkup(button),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await ShizukuMusic.join_call(
                chat_id, original_chat_id, file_path, video=status
            )
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            if video:
                await add_active_video_chat(chat_id)
            button = stream_markup(chat_id)
            mz = "<b> Started Streaming</b>\n\n<b>Title:</b> <a href={}>{}</a>\n<b>Duration:</b> {} minutes\n<b>Requested by:</b> {}"
            run = await app.send_message(
                original_chat_id,
                text=mz.format(link, title[:30], duration_min, user_name),
                reply_markup=InlineKeyboardMarkup(button),
                disable_web_page_preview=True
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
    elif streamtype == "live":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        duration_min = "Live Track"
        status = True if video else None
        if await is_active_chat(chat_id):
            check = db.get(chat_id)
            if len(check) > config.QUEUE_LIMIT:
                return await app.send_message(
                    chat_id,
                    f"You are spamming. {config.QUEUE_LIMIT} songs in queue, either wait them to finish or use /end.",
                )
            await put_queue(
                chat_id,
                original_chat_id,
                f"live_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            button = aq_markup(chat_id)
            q = "<b>Added to queue at #{}\n\nTitle:</b> {}\n<b>Duration:</b> {} minutes\n<b>Requested by:</b> {}"
            await app.send_message(
                chat_id=original_chat_id,
                text=q.format(position, title[:27], duration_min, user_name),
                reply_markup=InlineKeyboardMarkup(button),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            n, file_path = await YouTube.video(link)
            if n == 0:
                raise AssistantErr("No live youtube video found.")
            await ShizukuMusic.join_call(
                chat_id,
                original_chat_id,
                file_path,
                video=status,
            )
            await put_queue(
                chat_id,
                original_chat_id,
                f"live_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            button = stream_markup(chat_id)
            az = "<b> Started Streaming</b>\n\n<b>Title:</b> <a href={}>{}</a>\n<b>Duration:</b> {} minutes\n<b>Requested by:</b> {}"
            run = await app.send_message(
                original_chat_id,
                text=az.format(
                    f"https://t.me/{app.username}?start=info_{vidid}",
                    title[:30],
                    duration_min,
                    user_name,
                ),
                reply_markup=InlineKeyboardMarkup(button),
                disable_web_page_preview=True
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
    elif streamtype == "index":
        link = result
        title = "Index or M3U8 Link"
        duration_min = "00:00"
        if await is_active_chat(chat_id):
            check = db.get(chat_id)
            if len(check) > config.QUEUE_LIMIT:
                return await app.send_message(
                    chat_id,
                    f"You are spamming. {config.QUEUE_LIMIT} songs in queue, either wait them to finish or use /end.",
                )
            await put_queue_index(
                chat_id,
                original_chat_id,
                "index_url",
                title,
                duration_min,
                user_name,
                link,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            button = aq_markup(chat_id)
            mb = "<b>Added to queue at #{}\n\nTitle:</b> {}\n<b>Duration:</b> {} minutes\n<b>Requested by:</b> {}"
            await mystic.edit_text(
                text=mb.format(position, title[:27], duration_min, user_name),
                reply_markup=InlineKeyboardMarkup(button),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await ShizukuMusic.join_call(
                chat_id,
                original_chat_id,
                link,
                video=True if video else None,
            )
            await put_queue_index(
                chat_id,
                original_chat_id,
                "index_url",
                title,
                duration_min,
                user_name,
                link,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            button = stream_markup(chat_id)
            xc = "<b>Started Streaming</b>\n\n<b>Stream Type:</b> Live Stream [URL]\n<b>Requested by:</b> {}"

            run = await app.send_message(
                original_chat_id,
                text=xc.format(user_name),
                reply_markup=InlineKeyboardMarkup(button),
                disable_web_page_preview=True
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await mystic.delete()
