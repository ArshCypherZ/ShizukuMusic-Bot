from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import adminlist, confirmer
from Shizuku import app
from Shizuku.misc import db
from Shizuku.utils.database import (
    get_cmode,
    get_upvote_count,
    is_active_chat,
    is_nonadmin_chat,
    is_skipmode,
)


def AdminRightsCheck(mystic):
    async def wrapper(client, message):
        try:
            await message.delete()
        except BaseException:
            pass

        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="How to fix?",
                            callback_data="AnonymousAdmin",
                        ),
                    ]
                ]
            )
            return await message.reply_text(
                "You are anonymous admin, revert back to user account.",
                reply_markup=upl,
            )
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await message.reply_text(
                    "Please provide channel id through /channelplay"
                )
            try:
                await app.get_chat(chat_id)
            except BaseException:
                return await message.reply_text("Promote me as admin of the channel.")
        else:
            chat_id = message.chat.id
        if not await is_active_chat(chat_id):
            return await message.reply_text("Bot is not streaming on video chat.")
        is_non_admin = await is_nonadmin_chat(message.chat.id)
        if not is_non_admin:
            admins = adminlist.get(message.chat.id)
            if not admins:
                return await message.reply_text("Refresh admin cache via /reload")
            else:
                if message.from_user.id not in admins:
                    if await is_skipmode(message.chat.id):
                        upvote = await get_upvote_count(chat_id)
                        text = f"""<b>Admin rights needed</b>

Refresh admin cache : /reload

» {upvote} votes needed to perform this action."""

                        command = message.command[0]
                        if command[0] == "c":
                            command = command[1:]
                        if command == "speed":
                            return await message.reply_text(
                                "You do not have permissions to manage video chat. Do /reload if i am wrong."
                            )
                        MODE = command.title()
                        upl = InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        text="Vote",
                                        callback_data=f"ADMIN  UpVote|{chat_id}_{MODE}",
                                    ),
                                ]
                            ]
                        )
                        if chat_id not in confirmer:
                            confirmer[chat_id] = {}
                        try:
                            vidid = db[chat_id][0]["vidid"]
                            file = db[chat_id][0]["file"]
                        except BaseException:
                            return await message.reply_text(
                                "You do not have manage video chat permission. Do /reload if you think i am wrong."
                            )
                        senn = await message.reply_text(text, reply_markup=upl)
                        confirmer[chat_id][senn.id] = {
                            "vidid": vidid,
                            "file": file,
                        }
                        return
                    else:
                        return await message.reply_text(
                            "No right to manage video chat. Do /reload if you have."
                        )

        return await mystic(client, message, chat_id)

    return wrapper


def AdminActual(mystic):
    async def wrapper(client, message):
        try:
            await message.delete()
        except BaseException:
            pass

        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="How to fix?",
                            callback_data="AnonymousAdmin",
                        ),
                    ]
                ]
            )
            return await message.reply_text(
                "You are anonymous admin, revert back to user account.",
                reply_markup=upl,
            )

        try:
            member = (
                await app.get_chat_member(message.chat.id, message.from_user.id)
            ).privileges
        except BaseException:
            return
        if not member.can_manage_video_chats:
            return await message.reply(
                "No rights to manage video chat. Try /reload to refresh admin rights."
            )
        return await mystic(client, message)

    return wrapper


def ActualAdminCB(mystic):
    async def wrapper(client, CallbackQuery):
        if CallbackQuery.message.chat.type == ChatType.PRIVATE:
            return await mystic(client, CallbackQuery)
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            try:
                a = (
                    await app.get_chat_member(
                        CallbackQuery.message.chat.id,
                        CallbackQuery.from_user.id,
                    )
                ).privileges
            except BaseException:
                return await CallbackQuery.answer(
                    "Not enough required rights.", show_alert=True
                )
            if not a.can_manage_video_chats:
                return await CallbackQuery.answer(
                    "Not enough required rights by you.", show_alert=True
                )
        return await mystic(client, CallbackQuery)

    return wrapper
