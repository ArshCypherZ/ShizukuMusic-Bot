from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import MessageNotModified
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from config import OWNER_ID
from Shizuku import app
from Shizuku.utils.database import (
    add_nonadmin_chat,
    get_playmode,
    get_playtype,
    get_upvote_count,
    is_nonadmin_chat,
    is_skipmode,
    remove_nonadmin_chat,
    set_playmode,
    set_playtype,
    set_upvotes,
    skip_off,
    skip_on,
)
from Shizuku.utils.decorators.admins import ActualAdminCB
from Shizuku.utils.inline.settings import (
    playmode_users_markup,
    setting_markup,
    vote_mode_markup,
)
from Shizuku.utils.inline.start import private_panel

setting_1 = "<b>{} Settings Panel</b>\n\n<b>Chat ID :</b> <code>{}</code>\n<b>Chat Title :</b> {}\n\nClick on the buttons below for changing settings."
setting_2 = "» Direct: Plays search queries directly.\n\n» Inline: Returns inline buttons for choosing between video & audio."
setting_3 = "» Everyone: Anyone can use admin commands [skip, pause, resume, etc.] present in this group.\n\n» Admin Only: Only admins and authorized users can use admin commands."
setting_4 = "» No authorized users found."
setting_5 = "» Group: Plays music in the group where the command is given.\n\n» Channel: Plays music in the channel you want. Set channel ID via /channelplay"
setting_6 = "» Everyone: Anyone present in this group can play music here.\n\n» Admin Only: Only admins can play the music in this group."
setting_7 = "» Please define channel ID via /channelplay"
setting_8 = "When this mode is enabled, people without admin rights can use admin commands after a certain amount of votes."
setting_9 = "Current upvotes required for using admin commands are: {}"
setting_10 = "Voting mode is disabled."
setting_11 = "Lowest upvotes count can be 2. You can't set below 2."
setting_12 = "Highest upvotes count can be 15. You can't set above 15"


@app.on_message(filters.command(["settings", "setting"]) & filters.group)
async def settings_mar(client, message: Message):
    buttons = setting_markup()
    await message.reply_text(
        setting_1.format(app.mention, message.chat.id, message.chat.title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("settings_helper"))
async def settings_cb(client, CallbackQuery):
    buttons = setting_markup()
    return await CallbackQuery.edit_message_text(
        setting_1.format(
            app.mention,
            CallbackQuery.message.chat.id,
            CallbackQuery.message.chat.title,
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("settingsback_helper"))
async def settings_back_markup(client, CallbackQuery: CallbackQuery):
    try:
        await CallbackQuery.answer()
    except BaseException:
        pass
    if CallbackQuery.message.chat.type == ChatType.PRIVATE:
        await app.resolve_peer(OWNER_ID)
        buttons = private_panel()
        return await CallbackQuery.edit_message_text(
            "Hey {}, I'm {}, the Telegram bot that plays music in voice chats. I keep things simple and lightweight, making your chat experience extra enjoyable with some awesome tunes.".format(
                CallbackQuery.from_user.mention, app.mention
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = setting_markup()
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )


@app.on_callback_query(
    filters.regex(
        pattern=r"^(SEARCHANSWER|PLAYMODEANSWER|PLAYTYPEANSWER|AUTHANSWER|ANSWERVOMODE|VOTEANSWER|PM|AU|VM)$"
    )
)
async def without_Admin_rights(client, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    if command == "SEARCHANSWER":
        try:
            return await CallbackQuery.answer(setting_2, show_alert=True)
        except BaseException:
            return
    if command == "PLAYMODEANSWER":
        try:
            return await CallbackQuery.answer(setting_5, show_alert=True)
        except BaseException:
            return
    if command == "PLAYTYPEANSWER":
        try:
            return await CallbackQuery.answer(setting_6, show_alert=True)
        except BaseException:
            return
    if command == "AUTHANSWER":
        try:
            return await CallbackQuery.answer(setting_3, show_alert=True)
        except BaseException:
            return
    if command == "VOTEANSWER":
        try:
            return await CallbackQuery.answer(
                setting_8,
                show_alert=True,
            )
        except BaseException:
            return
    if command == "ANSWERVOMODE":
        current = await get_upvote_count(CallbackQuery.message.chat.id)
        try:
            return await CallbackQuery.answer(
                setting_9.format(current),
                show_alert=True,
            )
        except BaseException:
            return
    if command == "PM":
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            Group = True
        else:
            Group = None
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            Playtype = None
        else:
            Playtype = True
        buttons = playmode_users_markup(Direct, Group, Playtype)
    if command == "VM":
        mode = await is_skipmode(CallbackQuery.message.chat.id)
        current = await get_upvote_count(CallbackQuery.message.chat.id)
        buttons = vote_mode_markup(current, mode)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


@app.on_callback_query(filters.regex("FERRARIUDTI"))
@ActualAdminCB
async def addition(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    mode = callback_data.split(None, 1)[1]
    if not await is_skipmode(CallbackQuery.message.chat.id):
        return await CallbackQuery.answer(setting_10, show_alert=True)
    current = await get_upvote_count(CallbackQuery.message.chat.id)
    if mode == "M":
        final = current - 2
        if final == 0:
            return await CallbackQuery.answer(
                setting_11,
                show_alert=True,
            )
        if final <= 2:
            final = 2
        await set_upvotes(CallbackQuery.message.chat.id, final)
    else:
        final = current + 2
        if final == 17:
            return await CallbackQuery.answer(
                setting_12,
                show_alert=True,
            )
        if final >= 15:
            final = 15
        await set_upvotes(CallbackQuery.message.chat.id, final)
    buttons = vote_mode_markup(final, True)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


@app.on_callback_query(
    filters.regex(pattern=r"^(MODECHANGE|CHANNELMODECHANGE|PLAYTYPECHANGE)$")
)
@ActualAdminCB
async def playmode_ans(client, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    if command == "CHANNELMODECHANGE":
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            await add_nonadmin_chat(CallbackQuery.message.chat.id)
            Group = None
        else:
            await remove_nonadmin_chat(CallbackQuery.message.chat.id)
            Group = True
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            Playtype = None
        else:
            Playtype = True
        buttons = playmode_users_markup(Direct, Group, Playtype)
    if command == "MODECHANGE":
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            await set_playmode(CallbackQuery.message.chat.id, "Inline")
            Direct = None
        else:
            await set_playmode(CallbackQuery.message.chat.id, "Direct")
            Direct = True
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            Group = True
        else:
            Group = None
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            Playtype = False
        else:
            Playtype = True
        buttons = playmode_users_markup(Direct, Group, Playtype)
    if command == "PLAYTYPECHANGE":
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            await set_playtype(CallbackQuery.message.chat.id, "Admin")
            Playtype = False
        else:
            await set_playtype(CallbackQuery.message.chat.id, "Everyone")
            Playtype = True
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            Group = True
        else:
            Group = None
        buttons = playmode_users_markup(Direct, Group, Playtype)
    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


@app.on_callback_query(filters.regex("VOMODECHANGE"))
@ActualAdminCB
async def vote_change(client, CallbackQuery):
    CallbackQuery.matches[0].group(1)
    mod = None
    if await is_skipmode(CallbackQuery.message.chat.id):
        await skip_off(CallbackQuery.message.chat.id)
    else:
        mod = True
        await skip_on(CallbackQuery.message.chat.id)
    current = await get_upvote_count(CallbackQuery.message.chat.id)
    buttons = vote_mode_markup(current, mod)

    try:
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return
