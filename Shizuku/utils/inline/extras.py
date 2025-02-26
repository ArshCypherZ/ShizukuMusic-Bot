from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import SUPPORT_CHAT


def botplaylist_markup():
    buttons = [
        [
            InlineKeyboardButton(text="Support Group", url=SUPPORT_CHAT),
            InlineKeyboardButton(text="Close", callback_data="close"),
        ],
    ]
    return buttons


def close_markup():
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Close",
                    callback_data="close",
                ),
            ]
        ]
    )
    return upl


def supp_markup():
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Support Group",
                    url=SUPPORT_CHAT,
                ),
            ]
        ]
    )
    return upl
