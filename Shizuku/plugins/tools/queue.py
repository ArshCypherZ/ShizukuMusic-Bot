import asyncio

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import CallbackQuery, Message

from Shizuku import app
from Shizuku.misc import db
from Shizuku.utils import get_channeplayCB, paste, seconds_to_min
from Shizuku.utils.database import get_cmode, is_active_chat, is_music_playing
from Shizuku.utils.inline import queue_back_markup, queue_markup

basic = {}


def get_duration(playing):
    file_path = playing[0]["file"]
    if "index_" in file_path or "live_" in file_path:
        return "Unknown"
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return "Unknown"
    else:
        return "Inline"


@app.on_message(
    filters.command(["queue", "cqueue", "player", "cplayer", "playing", "cplaying"])
    & filters.group
)
async def get_queue(client, message: Message):
    if message.command[0][0] == "c":
        chat_id = await get_cmode(message.chat.id)
        if chat_id is None:
            return await message.reply_text(
                "Please provide channel id via /channelplay"
            )
        try:
            await app.get_chat(chat_id)
        except BaseException:
            return await message.reply_text(
                "Make sure to add me as admin in the channel."
            )
        cplay = True
    else:
        chat_id = message.chat.id
        cplay = False
    if not await is_active_chat(chat_id):
        return await message.reply_text("Bot is not streaming in this chat.")
    got = db.get(chat_id)
    if not got:
        return await message.reply_text("Nothing is playing.")
    got[0]["file"]
    videoid = got[0]["vidid"]
    user = got[0]["by"]
    title = (got[0]["title"]).title()
    typo = (got[0]["streamtype"]).title()
    DUR = get_duration(got)
    g = "<b>Duration:</b> Unknown\n\nClick on button below to get whole queue."
    send = g if DUR == "Unknown" else "Click on button below to get whole queue."
    h = "<b>{} Player</b>\n\n<b>Streaming:</b> {}\n\n<b>Stream Type:</b> {}\n<b>Requested By:</b> {}\n{}"
    cap = h.format(app.mention, title, typo, user, send)
    upl = (
        queue_markup(DUR, "c" if cplay else "g", videoid)
        if DUR == "Unknown"
        else queue_markup(
            DUR,
            "c" if cplay else "g",
            videoid,
            seconds_to_min(got[0]["played"]),
            got[0]["dur"],
        )
    )
    basic[videoid] = True
    mystic = await message.reply_text(text=cap, reply_markup=upl)
    if DUR != "Unknown":
        try:
            while db[chat_id][0]["vidid"] == videoid:
                await asyncio.sleep(5)
                if await is_active_chat(chat_id):
                    if basic[videoid]:
                        if await is_music_playing(chat_id):
                            try:
                                buttons = queue_markup(
                                    DUR,
                                    "c" if cplay else "g",
                                    videoid,
                                    seconds_to_min(db[chat_id][0]["played"]),
                                    db[chat_id][0]["dur"],
                                )
                                await mystic.edit_reply_markup(reply_markup=buttons)
                            except FloodWait:
                                pass
                        else:
                            pass
                    else:
                        break
                else:
                    break
        except BaseException:
            return


@app.on_callback_query(filters.regex("GetTimer"))
async def quite_timer(client, CallbackQuery: CallbackQuery):
    try:
        await CallbackQuery.answer()
    except BaseException:
        pass


@app.on_callback_query(filters.regex("GetQueued"))
async def queued_tracks(client, CallbackQuery: CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    what, videoid = callback_request.split("|")
    try:
        chat_id, channel = await get_channeplayCB(what, CallbackQuery)
    except BaseException:
        return
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(
            "Bot isn't streaming on videochat.", show_alert=True
        )
    got = db.get(chat_id)
    if not got:
        return await CallbackQuery.answer("Nothing is playing.", show_alert=True)
    if len(got) == 1:
        return await CallbackQuery.answer(
            "Only one track in queue. Add more to list them.", show_alert=True
        )
    await CallbackQuery.answer()
    basic[videoid] = False
    buttons = queue_back_markup(what)
    await CallbackQuery.edit_message_text(text="Fetching please wait...")
    j = 0
    msg = ""
    for x in got:
        j += 1
        if j == 1:
            msg += f'Streaming :\n\n✨ Title : {x["title"]}\nDuration : {x["dur"]}\nBy : {x["by"]}\n\n'
        elif j == 2:
            msg += f'Queued :\n\n✨ Title : {x["title"]}\nDuration : {x["dur"]}\nBy : {x["by"]}\n\n'
        else:
            msg += f'✨ Title : {x["title"]}\nDuration : {x["dur"]}\nBy : {x["by"]}\n\n'
    if "Queued" in msg:
        if len(msg) < 700:
            await asyncio.sleep(1)
            return await CallbackQuery.edit_message_text(msg, reply_markup=buttons)
        if "✨" in msg:
            msg = msg.replace("✨", "")
        link = await paste(msg)
        t = "<u>Click here to check list of queued tracks:</u> <a href={0}>Here</a>"
        await CallbackQuery.edit_message_text(text=t.format(link), reply_markup=buttons)
    else:
        await asyncio.sleep(1)
        return await CallbackQuery.edit_message_text(msg, reply_markup=buttons)


@app.on_callback_query(filters.regex("queue_back_timer"))
async def queue_back(client, CallbackQuery: CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cplay = callback_data.split(None, 1)[1]
    try:
        chat_id, channel = await get_channeplayCB(cplay, CallbackQuery)
    except BaseException:
        return
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer("Bot is not streaming here.", show_alert=True)
    got = db.get(chat_id)
    if not got:
        return await CallbackQuery.answer("Nothing is playing.", show_alert=True)
    got[0]["file"]
    videoid = got[0]["vidid"]
    user = got[0]["by"]
    title = (got[0]["title"]).title()
    typo = (got[0]["streamtype"]).title()
    DUR = get_duration(got)
    send = (
        "Unknown duration of track. Click below button to get whole queue list."
        if DUR == "Unknown"
        else "Click below button to get whole queue list."
    )
    h = "<b>{} Player</b>\n\n<b>Streaming:</b> {}\n\n<b>Stream Type:</b> {}\n<b>Requested By:</b> {}\n{}"
    cap = h.format(app.mention, title, typo, user, send)
    upl = (
        queue_markup(DUR, cplay, videoid)
        if DUR == "Unknown"
        else queue_markup(
            DUR,
            cplay,
            videoid,
            seconds_to_min(got[0]["played"]),
            got[0]["dur"],
        )
    )
    basic[videoid] = True
    mystic = await CallbackQuery.edit_message_text(text=cap, reply_markup=upl)
    if DUR != "Unknown":
        try:
            while db[chat_id][0]["vidid"] == videoid:
                await asyncio.sleep(5)
                if await is_active_chat(chat_id):
                    if basic[videoid]:
                        if await is_music_playing(chat_id):
                            try:
                                buttons = queue_markup(
                                    DUR,
                                    cplay,
                                    videoid,
                                    seconds_to_min(db[chat_id][0]["played"]),
                                    db[chat_id][0]["dur"],
                                )
                                await mystic.edit_reply_markup(reply_markup=buttons)
                            except FloodWait:
                                pass
                        else:
                            pass
                    else:
                        break
                else:
                    break
        except BaseException:
            return
