from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

import helpers
from config import SUPPORT_CHAT
from Shizuku import app
from Shizuku.utils import help_pannel
from Shizuku.utils.inline.help import help_back_markup, private_help_panel


@app.on_message(filters.command(["help"]) & filters.private)
@app.on_callback_query(filters.regex("settings_back_helper"))
async def helper_private(
    client: app, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except BaseException:
            pass
        keyboard = help_pannel(True)
        await update.edit_message_text(
            "Select a topic below for assistance, or join {} for any questions.".format(
                SUPPORT_CHAT
            ),
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    else:
        try:
            await update.delete()
        except BaseException:
            pass
        keyboard = help_pannel()
        await update.reply_text(
            "Select a topic below for assistance, or join {} for any questions.".format(
                SUPPORT_CHAT
            ),
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(["help"]) & filters.group)
async def help_com_group(client, message: Message):
    keyboard = private_help_panel()
    await message.reply_text(
        "Click below button for help!", reply_markup=InlineKeyboardMarkup(keyboard)
    )


@app.on_callback_query(filters.regex("help_callback"))
async def helper_cb(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup()
    if cb == "hb1":
        await CallbackQuery.edit_message_text(helpers.HELP_1, reply_markup=keyboard)
    elif cb == "hb2":
        await CallbackQuery.edit_message_text(helpers.HELP_2, reply_markup=keyboard)
    elif cb == "hb3":
        await CallbackQuery.edit_message_text(helpers.HELP_3, reply_markup=keyboard)
    elif cb == "hb4":
        await CallbackQuery.edit_message_text(helpers.HELP_4, reply_markup=keyboard)
    elif cb == "hb5":
        await CallbackQuery.edit_message_text(helpers.HELP_5, reply_markup=keyboard)
    elif cb == "hb6":
        await CallbackQuery.edit_message_text(helpers.HELP_6, reply_markup=keyboard)
    elif cb == "hb7":
        await CallbackQuery.edit_message_text(helpers.HELP_7, reply_markup=keyboard)
    elif cb == "hb8":
        await CallbackQuery.edit_message_text(helpers.HELP_8, reply_markup=keyboard)
    elif cb == "hb9":
        await CallbackQuery.edit_message_text(helpers.HELP_9, reply_markup=keyboard)
    elif cb == "hb10":
        await CallbackQuery.edit_message_text(helpers.HELP_10, reply_markup=keyboard)
    elif cb == "hb11":
        await CallbackQuery.edit_message_text(helpers.HELP_11, reply_markup=keyboard)
    elif cb == "hb12":
        await CallbackQuery.edit_message_text(helpers.HELP_12, reply_markup=keyboard)
    elif cb == "hb13":
        await CallbackQuery.edit_message_text(helpers.HELP_13, reply_markup=keyboard)
    elif cb == "hb14":
        await CallbackQuery.edit_message_text(helpers.HELP_14, reply_markup=keyboard)
    elif cb == "hb15":
        await CallbackQuery.edit_message_text(helpers.HELP_15, reply_markup=keyboard)
