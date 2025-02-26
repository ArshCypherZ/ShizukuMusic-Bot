from pyrogram import filters
import logging

from Shizuku import YouTube, app
from Shizuku.utils.channelplay import get_channeplayCB
from Shizuku.utils.stream.stream import stream

play_2 = (
    "<b>Channel Play Mode</b>\n\nProcessing please wait...\n\n<b>Linked Channel:</b> {}"
)
play_1 = "🔎"
play_3 = "Failed to process query."


@app.on_callback_query(filters.regex("LiveStream"))
async def play_live_stream(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    vidid, user_id, mode, cplay, fplay = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer("Not for you.", show_alert=True)
        except BaseException:
            return
    try:
        chat_id, channel = await get_channeplayCB(cplay, CallbackQuery)
    except BaseException:
        return
    video = True if mode == "v" else None
    user_name = CallbackQuery.from_user.first_name
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except BaseException:
        pass
    mystic = await CallbackQuery.message.reply_text(
        play_2.format(channel) if channel else play_1
    )
    try:
        details, track_id = await YouTube.track(vidid, True)
    except Exception as e:
        logging.error(e)
        return await mystic.edit_text(play_3)
    ffplay = True if fplay == "f" else None
    if not details["duration_min"]:
        try:
            await stream(
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                CallbackQuery.message.chat.id,
                video,
                streamtype="live",
                forceplay=ffplay,
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else "Error {}".format(e)
            return await mystic.edit_text(err)
    else:
        return await mystic.edit_text("Cannot find a live stream.")
    await mystic.delete()
