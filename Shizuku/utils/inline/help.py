from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Shizuku import app


def help_pannel(START: Union[bool, int] = None):
    first = [InlineKeyboardButton(text="Close", callback_data=f"close")]
    second = [
        InlineKeyboardButton(
            text="Back",
            callback_data=f"settingsback_helper",
        ),
    ]
    mark = second if START else first
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Admins",
                    callback_data="help_callback hb1",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Broadcast",
                    callback_data="help_callback hb3",
                ),
                InlineKeyboardButton(
                    text="Channel Playback",
                    callback_data="help_callback hb6",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Loop",
                    callback_data="help_callback hb8",
                ),
                InlineKeyboardButton(
                    text="Play",
                    callback_data="help_callback hb11",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Shuffle",
                    callback_data="help_callback hb12",
                ),
                InlineKeyboardButton(
                    text="Seek",
                    callback_data="help_callback hb13",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Song",
                    callback_data="help_callback hb14",
                ),
                InlineKeyboardButton(
                    text="Speed",
                    callback_data="help_callback hb15",
                ),
            ],
            mark,
        ]
    )
    return upl


def help_back_markup():
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Back",
                    callback_data=f"settings_back_helper",
                ),
            ]
        ]
    )
    return upl


def private_help_panel():
    buttons = [
        [
            InlineKeyboardButton(
                text="Commands",
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]
    return buttons
