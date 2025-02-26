from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import adminlist, confirmer, votemode
from Shizuku import app
from Shizuku.core.call import ShizukuMusic
from Shizuku.misc import db
from Shizuku.utils.database import (
    get_upvote_count,
    is_active_chat,
    is_music_playing,
    is_nonadmin_chat,
    music_off,
    music_on,
)
from Shizuku.utils.inline import close_markup

checker = {}
upvoters = {}


@app.on_callback_query(filters.regex("ADMIN"))
async def del_back_playlist(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    command, chat = callback_request.split("|")
    if "_" in str(chat):
        bet = chat.split("_")
        chat = bet[0]
        counter = bet[1]
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(
            "Bot is not streaming in VC.", show_alert=True
        )
    mention = CallbackQuery.from_user.mention
    if command == "UpVote":
        if chat_id not in votemode:
            votemode[chat_id] = {}
        if chat_id not in upvoters:
            upvoters[chat_id] = {}

        voters = (upvoters[chat_id]).get(CallbackQuery.message.id)
        if not voters:
            upvoters[chat_id][CallbackQuery.message.id] = []

        vote = (votemode[chat_id]).get(CallbackQuery.message.id)
        if not vote:
            votemode[chat_id][CallbackQuery.message.id] = 0

        if CallbackQuery.from_user.id in upvoters[chat_id][CallbackQuery.message.id]:
            (upvoters[chat_id][CallbackQuery.message.id]).remove(
                CallbackQuery.from_user.id
            )
            votemode[chat_id][CallbackQuery.message.id] -= 1
        else:
            (upvoters[chat_id][CallbackQuery.message.id]).append(
                CallbackQuery.from_user.id
            )
            votemode[chat_id][CallbackQuery.message.id] += 1
        upvote = await get_upvote_count(chat_id)
        get_upvotes = int(votemode[chat_id][CallbackQuery.message.id])
        if get_upvotes >= upvote:
            votemode[chat_id][CallbackQuery.message.id] = upvote
            try:
                exists = confirmer[chat_id][CallbackQuery.message.id]
                current = db[chat_id][0]
            except Exception as e:
                return await CallbackQuery.edit_message_text(f"Failed due to {e}")
            try:
                if current["vidid"] != exists["vidid"]:
                    return await CallbackQuery.edit_message.text(
                        "The voting has ended because the track ended for which the voting was done for."
                    )
                if current["file"] != exists["file"]:
                    return await CallbackQuery.edit_message.text(
                        "The voting has ended because the track ended for which the voting was done for."
                    )
            except BaseException:
                return await CallbackQuery.edit_message_text(
                    "Failed to perform this action."
                )
            try:
                await CallbackQuery.edit_message_text(
                    "Succesfully got {} upvotes.".format(upvote)
                )
            except BaseException:
                pass
            command = counter
            mention = "Upvotes"
        else:
            if (
                CallbackQuery.from_user.id
                in upvoters[chat_id][CallbackQuery.message.id]
            ):
                await CallbackQuery.answer("Added 1 upvote", show_alert=True)
            else:
                await CallbackQuery.answer("Removed 1 upvote", show_alert=True)
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=f"👍 {get_upvotes}",
                            callback_data=f"ADMIN  UpVote|{chat_id}_{counter}",
                        )
                    ]
                ]
            )
            await CallbackQuery.answer("Upvoted", show_alert=True)
            return await CallbackQuery.edit_message_reply_markup(reply_markup=upl)
    else:
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
                        "You are missing manage video chat right in this chat, if i am wrong do /reload",
                        show_alert=True,
                    )
    if command == "Pause":
        if not await is_music_playing(chat_id):
            return await CallbackQuery.answer(
                "Stream is already paused.", show_alert=True
            )
        await CallbackQuery.answer()
        await music_off(chat_id)
        await ShizukuMusic.pause_stream(chat_id)
        await CallbackQuery.message.reply_text(
            "Stream is paused by {}".format(mention), reply_markup=close_markup()
        )
    elif command == "Resume":
        if await is_music_playing(chat_id):
            return await CallbackQuery.answer(
                "Stream is already resumed.", show_alert=True
            )
        await CallbackQuery.answer()
        await music_on(chat_id)
        await ShizukuMusic.resume_stream(chat_id)
        await CallbackQuery.message.reply_text(
            "Stream has been resumed by {}".format(mention), reply_markup=close_markup()
        )
