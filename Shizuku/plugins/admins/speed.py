from pyrogram import filters
from pyrogram.types import Message

from config import adminlist
from Shizuku import app
from Shizuku.core.call import ShizukuMusic
from Shizuku.misc import db
from Shizuku.utils import AdminRightsCheck
from Shizuku.utils.database import is_active_chat, is_nonadmin_chat
from Shizuku.utils.inline import close_markup, speed_markup

checker = []


@app.on_message(
    filters.command(["cspeed", "speed", "cslow", "slow", "playback", "cplayback"])
    & filters.group
)
@AdminRightsCheck
async def playback(cli, message: Message, chat_id):
    playing = db.get(chat_id)
    if not playing:
        return await message.reply_text("Queue is empty.")
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await message.reply_text("Only youtube steams can be speed up or down.")
    file_path = playing[0]["file"]
    if "downloads" not in file_path:
        return await message.reply_text("Only youtube steams can be speed up or down.")
    upl = speed_markup(chat_id)
    return await message.reply_text(
        text="Choose the speed you want to set for the stream.",
        reply_markup=upl,
    )


@app.on_callback_query(filters.regex("SpeedUP"))
async def del_back_playlist(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    chat, speed = callback_request.split("|")
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer("Bot is not streaming.", show_alert=True)
    is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
    if not is_non_admin:
        admins = adminlist.get(CallbackQuery.message.chat.id)
        if not admins:
            return await CallbackQuery.answer(
                "Refresh admin cache via /reload", show_alert=True
            )
        else:
            if CallbackQuery.from_user.id not in admins:
                return await CallbackQuery.answer(
                    "You do not have permissions to manage video chat. Do /reload if you think i am wrong.",
                    show_alert=True,
                )
    playing = db.get(chat_id)
    if not playing:
        return await CallbackQuery.answer("Queue is empty.", show_alert=True)
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await CallbackQuery.answer(
            "Only youtube streams can be speed up or down.", show_alert=True
        )
    file_path = playing[0]["file"]
    if "downloads" not in file_path:
        return await CallbackQuery.answer(
            "Only youtube streams can be speed up or down.", show_alert=True
        )
    checkspeed = (playing[0]).get("speed")
    if checkspeed:
        if str(checkspeed) == str(speed):
            if str(speed) == str("1.0"):
                return await CallbackQuery.answer(
                    "Bot is already on normal speed.",
                    show_alert=True,
                )
    else:
        if str(speed) == str("1.0"):
            return await CallbackQuery.answer(
                "Bot is already on normal speed.",
                show_alert=True,
            )
    if chat_id in checker:
        return await CallbackQuery.answer(
            "Please wait, someone else is already trying to change the speed.",
            show_alert=True,
        )
    else:
        checker.append(chat_id)
    try:
        await CallbackQuery.answer(
            "Changing speed.",
        )
    except BaseException:
        pass
    mystic = await CallbackQuery.edit_message_text(
        text="Trying to change the speed, requested by {}".format(
            CallbackQuery.from_user.mention
        ),
    )
    try:
        await ShizukuMusic.speedup_stream(
            chat_id,
            file_path,
            speed,
            playing,
        )
    except BaseException:
        if chat_id in checker:
            checker.remove(chat_id)
        return await mystic.edit_text(
            "Failed to change the speed.", reply_markup=close_markup()
        )
    if chat_id in checker:
        checker.remove(chat_id)
    await mystic.edit_text(
        text="Changing the stream speed to {}. Requested by {}".format(
            speed, CallbackQuery.from_user.mention
        ),
        reply_markup=close_markup(),
    )
