from pyrogram.types import InlineKeyboardButton

import config
from Shizuku import app


def start_panel():
    buttons = [
        [
            InlineKeyboardButton(
                text="Add Me", url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text="Support Group", url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons


def private_panel():
    buttons = [
        [
            InlineKeyboardButton(
                text="Add Me", url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text="Commands", callback_data="settings_back_helper"),
        ],
        [
            InlineKeyboardButton(text="Support Group", url=config.SUPPORT_CHAT),
            InlineKeyboardButton(text="News Channel", url=config.SUPPORT_CHANNEL),
        ],
    ]
    return buttons
