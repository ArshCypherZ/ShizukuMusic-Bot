from Shizuku import app
from Shizuku.utils.database import get_cmode


async def get_channeplayCB(command, CallbackQuery):
    if command == "c":
        chat_id = await get_cmode(CallbackQuery.message.chat.id)
        if chat_id is None:
            try:
                return await CallbackQuery.answer(
                    "Please input channel id through /channelplay", show_alert=True
                )
            except BaseException:
                return
        try:
            channel = (await app.get_chat(chat_id)).title
        except BaseException:
            try:
                return await CallbackQuery.answer(
                    "Make sure bot is promoted as admin in the channel.",
                    show_alert=True,
                )
            except BaseException:
                return
    else:
        chat_id = CallbackQuery.message.chat.id
        channel = None
    return chat_id, channel
