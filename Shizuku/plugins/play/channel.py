from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.types import Message

from Shizuku import app
from Shizuku.utils.database import set_cmode
from Shizuku.utils.decorators.admins import AdminActual

cplay_1 = "You can play music in channel from {} to any channel or your chat's linked channel.\n\n<b>For linked channel:</b>\n<code>/channelplay linked</code>\n\n<b>For any other channel:</b>\n<code>/channelplay [channel id]</code>"
cplay_2 = "This chat does not have any linked channel."
cplay_3 = "Channel defined to {}.\nChannel ID: <code>{}</code>"
cplay_4 = "Promote me in channel as admin."
cplay_5 = "Only channels are supported."
cplay_6 = "Be an owner of {} to connect it with this group.\n<b>Channel's Owner:</b> @{}\n\nAlternatively you can link your group with that channel and then try connecting with <code>/channelplay linked</code>"
cplay_7 = "Channel play is disabled."


@app.on_message(filters.command(["channelplay"]) & filters.group)
@AdminActual
async def playmode_(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(cplay_1.format(message.chat.title))
    query = message.text.split(None, 2)[1].lower().strip()
    if (str(query)).lower() == "disable":
        await set_cmode(message.chat.id, None)
        return await message.reply_text(cplay_7)
    elif str(query) == "linked":
        chat = await app.get_chat(message.chat.id)
        if chat.linked_chat:
            chat_id = chat.linked_chat.id
            await set_cmode(message.chat.id, chat_id)
            return await message.reply_text(
                cplay_3.format(chat.linked_chat.title, chat.linked_chat.id)
            )
        else:
            return await message.reply_text(cplay_2)
    else:
        try:
            chat = await app.get_chat(query)
        except BaseException:
            return await message.reply_text(cplay_4)
        if chat.type != ChatType.CHANNEL:
            return await message.reply_text(cplay_5)
        try:
            async for user in app.get_chat_members(
                chat.id, filter=ChatMembersFilter.ADMINISTRATORS
            ):
                if user.status == ChatMemberStatus.OWNER:
                    cusn = user.user.username
                    crid = user.user.id
        except BaseException:
            return await message.reply_text(cplay_4)
        if crid != message.from_user.id:
            return await message.reply_text(cplay_6.format(chat.title, cusn))
        await set_cmode(message.chat.id, chat.id)
        return await message.reply_text(cplay_3.format(chat.title, chat.id))
