from typing import Union

from pyrogram.types import InlineKeyboardButton


def setting_markup():
    buttons = [
        [
            InlineKeyboardButton(text="Play Mode", callback_data="PM"),
        ],
        [
            InlineKeyboardButton(text="Voting Mode", callback_data="VM"),
        ],
        [
            InlineKeyboardButton(text="Close", callback_data="close"),
        ],
    ]
    return buttons


def vote_mode_markup(current, mode: Union[bool, str] = None):
    buttons = [
        [
            InlineKeyboardButton(text="Voting Mode >", callback_data="VOTEANSWER"),
            InlineKeyboardButton(
                text="ON" if mode else "OFF",
                callback_data="VOMODECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(text="-2", callback_data="FERRARIUDTI M"),
            InlineKeyboardButton(
                text=f"Current: {current}",
                callback_data="ANSWERVOMODE",
            ),
            InlineKeyboardButton(text="+2", callback_data="FERRARIUDTI A"),
        ],
        [
            InlineKeyboardButton(
                text="Back",
                callback_data="settings_helper",
            ),
            InlineKeyboardButton(text="Close", callback_data="close"),
        ],
    ]
    return buttons


def playmode_users_markup(
    Direct: Union[bool, str] = None,
    Group: Union[bool, str] = None,
    Playtype: Union[bool, str] = None,
):
    buttons = [
        [
            InlineKeyboardButton(text="Search Mode >", callback_data="SEARCHANSWER"),
            InlineKeyboardButton(
                text="Direct" if Direct else "Inline",
                callback_data="MODECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(text="Admin Commands >", callback_data="AUTHANSWER"),
            InlineKeyboardButton(
                text="Admins" if Group else "Everyone",
                callback_data="CHANNELMODECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(text="Play Type >", callback_data="PLAYTYPEANSWER"),
            InlineKeyboardButton(
                text="Admins" if Playtype else "Everyone",
                callback_data="PLAYTYPECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(
                text="Back",
                callback_data="settings_helper",
            ),
            InlineKeyboardButton(text="Close", callback_data="close"),
        ],
    ]
    return buttons
