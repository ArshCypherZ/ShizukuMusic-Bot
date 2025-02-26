from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def stats_buttons(status):
    not_sudo = [
        InlineKeyboardButton(
            text="Overall Stats",
            callback_data="TopOverall",
        )
    ]
    sudo = [
        InlineKeyboardButton(
            text="General",
            callback_data="bot_stats_sudo",
        ),
        InlineKeyboardButton(
            text="Overall",
            callback_data="TopOverall",
        ),
    ]
    upl = InlineKeyboardMarkup(
        [
            sudo if status else not_sudo,
            [
                InlineKeyboardButton(
                    text="Close",
                    callback_data="close",
                ),
            ],
        ]
    )
    return upl


def back_stats_buttons():
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Back",
                    callback_data="stats_back",
                ),
                InlineKeyboardButton(
                    text="Close",
                    callback_data="close",
                ),
            ],
        ]
    )
    return upl
