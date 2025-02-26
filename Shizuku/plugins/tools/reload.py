import asyncio
import time

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus
from pyrogram.types import CallbackQuery, Message

from config import adminlist, lyrical
from Shizuku import app
from Shizuku.core.call import ShizukuMusic
from Shizuku.misc import db
from Shizuku.utils.database import get_assistant, get_cmode
from Shizuku.utils.decorators import ActualAdminCB, AdminActual
from Shizuku.utils.formatters import get_readable_time

rel = {}


@app.on_message(filters.command(["admincache", "reload", "refresh"]) & filters.group)
async def reload_admin_cache(client, message: Message):
    try:
        if message.chat.id not in rel:
            rel[message.chat.id] = {}
        else:
            saved = rel[message.chat.id]
            if saved > time.time():
                left = get_readable_time((int(saved) - int(time.time())))
                return await message.reply_text(
                    "You can only refresh admin cache once in every 3 minutes.\n\nPlease try after {}.".format(
                        left
                    )
                )
        adminlist[message.chat.id] = []
        async for user in app.get_chat_members(
            message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        ):
            if user.status == (ChatMemberStatus.ADMINISTRATOR or ChatMemberStatus.OWNER):
                adminlist[message.chat.id].append(user.user.id)
        now = int(time.time()) + 180
        rel[message.chat.id] = now
        await message.reply_text("Admin cache refreshed.")
    except BaseException:
        await message.reply_text("Please make me admin here first.")


@app.on_message(filters.command(["reboot"]) & filters.group)
@AdminActual
async def restartbot(client, message: Message):
    mystic = await message.reply_text("Wait...")
    await asyncio.sleep(1)
    try:
        db[message.chat.id] = []
        await ShizukuMusic.stop_stream_force(message.chat.id)
    except BaseException:
        pass
    userbot = await get_assistant(message.chat.id)
    try:
        if message.chat.username:
            await userbot.resolve_peer(message.chat.username)
        else:
            await userbot.resolve_peer(message.chat.id)
    except BaseException:
        pass
    chat_id = await get_cmode(message.chat.id)
    if chat_id:
        try:
            got = await app.get_chat(chat_id)
        except BaseException:
            pass
        userbot = await get_assistant(chat_id)
        try:
            if got.username:
                await userbot.resolve_peer(got.username)
            else:
                await userbot.resolve_peer(chat_id)
        except BaseException:
            pass
        try:
            db[chat_id] = []
            await ShizukuMusic.stop_stream_force(chat_id)
        except BaseException:
            pass
    await message.reply_text("Done, try playing now.")
    await mystic.delete()


@app.on_callback_query(filters.regex("close"))
async def close_menu(_, CallbackQuery):
    try:
        await CallbackQuery.answer()
        await CallbackQuery.message.delete()
        await CallbackQuery.message.reply_text(
            f"Closed By: {CallbackQuery.from_user.mention}"
        )
    except BaseException:
        pass


@app.on_callback_query(filters.regex("stop_downloading"))
@ActualAdminCB
async def stop_download(client, CallbackQuery: CallbackQuery):
    message_id = CallbackQuery.message.id
    task = lyrical.get(message_id)
    if not task:
        return await CallbackQuery.answer(
            "Download already completed.", show_alert=True
        )
    if task.done() or task.cancelled():
        return await CallbackQuery.answer(
            "Download already completed or cancelled.", show_alert=True
        )
    if not task.done():
        try:
            task.cancel()
            try:
                lyrical.pop(message_id)
            except BaseException:
                pass
            await CallbackQuery.answer("Download Cancelled.", show_alert=True)
            return await CallbackQuery.edit_message_text(
                "Download cancelled by {}".format(CallbackQuery.from_user.mention)
            )
        except BaseException:
            return await CallbackQuery.answer(
                "Failed to stop the downloading.", show_alert=True
            )
    await CallbackQuery.answer("Failed to find downloading task.", show_alert=True)
