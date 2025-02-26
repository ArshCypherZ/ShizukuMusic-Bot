import logging
import time

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from Shizuku import app
from Shizuku.misc import _boot_
from Shizuku.utils.database import add_served_chat, add_served_user
from Shizuku.utils.formatters import get_readable_time
from Shizuku.utils.inline import help_pannel, private_panel, start_panel


@app.on_message(filters.command(["start"]) & filters.private)
async def start_pm(client, message: Message):
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel()
            return await message.reply_text(
                text="Select a topic below for assistance, or join at <a href={}>Support Group</a> for any questions.".format(
                    config.SUPPORT_CHAT
                ),
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )

        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            me = "<b>Track information</b>\n\n📌 <b>Title:</b> {}\n\n<b>Duration:</b> {} minutes\n<b>Views:</b> <code>{}</code>\n<b>Published on:</b> {}\n<b>Channel:</b> <a href={}>{}</a>"
            searched_text = me.format(
                title, duration, views, published, channellink, channel
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Youtube", url=link),
                        InlineKeyboardButton(
                            text="Support Group", url=config.SUPPORT_CHAT
                        ),
                    ],
                ]
            )
            await m.delete()
            await app.send_message(
                chat_id=message.chat.id,
                text=searched_text,
                reply_markup=key,
            )
    else:
        out = private_panel()
        await message.reply_text(
            text="Hey <b>{}</b>, I'm <b>{}</b>, the Telegram bot that plays music in voice chats. I keep things simple and lightweight, making your chat experience extra enjoyable with some awesome tunes.".format(
                message.from_user.mention, app.mention
            ),
            reply_markup=InlineKeyboardMarkup(out),
        )


@app.on_message(filters.command(["start"]) & filters.group)
async def start_gp(client, message: Message):
    out = start_panel()
    uptime = int(time.time() - _boot_)
    await message.reply_text(
        text="Hey I am <b>{}</b>!\n<b>Uptime:</b> {}".format(
            app.mention, get_readable_time(uptime)
        ),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text("Need supergroup to work in.")
                    return await app.leave_chat(message.chat.id)

                out = start_panel()
                await message.reply_text(
                    text="Hey {}. Thanks for adding {} in {}.".format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            logging.error(ex)
