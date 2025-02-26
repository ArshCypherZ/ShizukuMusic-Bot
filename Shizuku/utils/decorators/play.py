import asyncio

from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import QUEUE_LIMIT, adminlist
from Shizuku import YouTube, app
from Shizuku.misc import db
from Shizuku.utils.database import (
    get_assistant,
    get_cmode,
    get_playmode,
    get_playtype,
    is_active_chat,
)
from Shizuku.utils.inline import botplaylist_markup

links = {}


def PlayWrapper(command):
    async def wrapper(client, message):
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
                "You are an anonymous admin in this chat, revert back to user account inorder to use me.",
                reply_markup=upl,
            )

        if await is_active_chat(message.chat.id):
            check = db.get(message.chat.id)
            if len(check) > QUEUE_LIMIT:
                return await message.reply_text(
                    text=f"You are spamming. {QUEUE_LIMIT} songs in queue, either wait them to finish or use /end."
                )
        try:
            await message.delete()
        except BaseException:
            pass

        audio_telegram = (
            (message.reply_to_message.audio or message.reply_to_message.voice)
            if message.reply_to_message
            else None
        )
        video_telegram = (
            (message.reply_to_message.video or message.reply_to_message.document)
            if message.reply_to_message
            else None
        )
        url = await YouTube.url(message)
        if audio_telegram is None and video_telegram is None and url is None:
            g = "<b>Usage:</b> /play [songname/youtube link/reply to audio or video file]"
            if len(message.command) < 2:
                if "stream" in message.command:
                    return await message.reply_text(
                        "Please provide M3U8 or Index link."
                    )
                buttons = botplaylist_markup()
                return await message.reply_text(
                    text=g,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await message.reply_text(
                    "Please provide me channel id via /channelplay"
                )
            try:
                chat = await app.get_chat(chat_id)
            except BaseException:
                return await message.reply_text(
                    "Make sure bot is promoted as admin in the channel."
                )
            channel = chat.title
        else:
            chat_id = message.chat.id
            channel = None
        playmode = await get_playmode(message.chat.id)
        playty = await get_playtype(message.chat.id)
        if playty != "Everyone":
            admins = adminlist.get(message.chat.id)
            if not admins:
                return await message.reply_text(
                    "Please refresh admin cache via /reload"
                )
            if message.from_user.id not in admins:
                return await message.reply_text(
                    "Only admins are allowed to play in this chat. To change this, do /playmode"
                )
        if message.command[0][0] == "v":
            video = True
        else:
            if "-v" in message.text:
                video = True
            else:
                video = True if message.command[0][1] == "v" else None
        if message.command[0][-1] == "e":
            if not await is_active_chat(chat_id):
                return await message.reply_text(
                    "Please turn on voice chat, else i can't stream."
                )
            fplay = True
        else:
            fplay = None

        if not await is_active_chat(chat_id):
            userbot = await get_assistant(chat_id)
            try:
                try:
                    get = await app.get_chat_member(chat_id, userbot.id)
                except ChatAdminRequired:
                    return await message.reply_text(
                        "I cannot invite my assisant here. Make me admin with invite users permission."
                    )
                if get.status in [
                    ChatMemberStatus.BANNED,
                    ChatMemberStatus.RESTRICTED,
                ]:
                    x = "<u>{} My assistant is banned here.</u>\n\n<b>ID:</b> <code>{}</code>\n<b>Name:</b> {}\n<b>Username:</b> @{}\n\nPlease unban the assistant and try again."
                    return await message.reply_text(
                        x.format(
                            app.mention, userbot.id, userbot.name, userbot.username
                        )
                    )
            except UserNotParticipant:
                if chat_id in links:
                    invitelink = links[chat_id]
                else:
                    if message.chat.username:
                        invitelink = message.chat.username
                        try:
                            await userbot.resolve_peer(invitelink)
                        except BaseException:
                            pass
                    else:
                        try:
                            invitelink = await app.export_chat_invite_link(chat_id)
                        except ChatAdminRequired:
                            return await message.reply_text(
                                "I cannot invite my assisant here. Make me admin with invite users permission."
                            )
                        except Exception as e:
                            c = "Failed to invite {} my assistant here.\n\nReason: <code>{}</code>"
                            return await message.reply_text(
                                c.format(app.mention, type(e).__name__)
                            )

                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                myu = await message.reply_text("Please wait.")
                try:
                    await userbot.join_chat(invitelink)
                    await asyncio.sleep(1)
                except InviteRequestSent:
                    try:
                        await app.approve_chat_join_request(chat_id, userbot.id)
                    except Exception as e:
                        c = "Failed to invite {} my assistant here.\n\nReason: <code>{}</code>"
                        return await message.reply_text(
                            c.format(app.mention, type(e).__name__)
                        )
                    await asyncio.sleep(3)
                    await message.reply_text("Try to stream now.")
                    await myu.delete()
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    c = "Failed to invite {} my assistant here.\n\nReason: <code>{}</code>"
                    return await message.reply_text(
                        c.format(app.mention, type(e).__name__)
                    )

                links[chat_id] = invitelink

                try:
                    await userbot.resolve_peer(chat_id)
                except BaseException:
                    pass

        return await command(
            client,
            message,
            chat_id,
            video,
            channel,
            playmode,
            url,
            fplay,
        )

    return wrapper
