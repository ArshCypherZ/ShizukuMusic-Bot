import platform
from sys import version as pyver

import psutil
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.__version__ import __version__ as pytgver

import config
from config import OWNER_ID
from Shizuku import app
from Shizuku.core.mongo import mongodb
from Shizuku.core.userbot import assistants
from Shizuku.plugins import ALL_MODULES
from Shizuku.utils.database import get_served_chats, get_served_users
from Shizuku.utils.inline.stats import back_stats_buttons, stats_buttons


@app.on_message(filters.command(["stats", "gstats"]))
async def stats_global(client, message: Message):
    upl = stats_buttons(True if message.from_user.id == OWNER_ID else False)
    await message.reply_text(
        text="Click here",
        reply_markup=upl,
    )


@app.on_callback_query(filters.regex("stats_back"))
async def home_stats(client, CallbackQuery):
    upl = stats_buttons(True if CallbackQuery.from_user.id == OWNER_ID else False)
    await CallbackQuery.edit_message_text(
        text="Click here",
        reply_markup=upl,
    )


@app.on_callback_query(filters.regex("TopOverall"))
async def overall_stats(client, CallbackQuery):
    upl = back_stats_buttons()
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    gs = "<b><u>Stats:</u></b>\n\n<b>Assistants:</b> <code>{}</code>\n<b>Chats:</b> <code>{}</code>\n<b>Users:</b> <code>{}</code>\n<b>Modules:</b> <code>{}</code>\n<b>Auto Leaving Assistant:</b> {}\n<b>Play duration limit:</b> {} minutes."
    text = gs.format(
        len(assistants),
        served_chats,
        served_users,
        len(ALL_MODULES),
        config.AUTO_LEAVING_ASSISTANT,
        config.DURATION_LIMIT_MIN,
    )

    await CallbackQuery.message.reply_text(text=text, reply_markup=upl)


@app.on_callback_query(filters.regex("bot_stats_sudo"))
async def bot_stats(client, CallbackQuery):
    if CallbackQuery.from_user.id != OWNER_ID:
        return await CallbackQuery.answer("Only for Arsh.", show_alert=True)
    upl = back_stats_buttons()
    p_core = psutil.cpu_count(logical=False)
    t_core = psutil.cpu_count(logical=True)
    ram = str(round(psutil.virtual_memory().total / (1024.0**3))) + " GB"
    try:
        cpu_freq = psutil.cpu_freq().current
        if cpu_freq >= 1000:
            cpu_freq = f"{round(cpu_freq / 1000, 2)} GHz"
        else:
            cpu_freq = f"{round(cpu_freq, 2)} MHz"
    except BaseException:
        cpu_freq = "Failed to fetch"
    hdd = psutil.disk_usage("/")
    total = hdd.total / (1024.0**3)
    used = hdd.used / (1024.0**3)
    free = hdd.free / (1024.0**3)
    call = await mongodb.command("dbstats")
    datasize = call["dataSize"] / 1024
    storage = call["storageSize"] / 1024
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    m = "<b><u>Stats:</u></b>\n\n<b>Modules:</b> <code>{}</code>\n<b>Platform:</b> <code>{}</code>\n<b>Ram:</b> <code>{}</code>\n<b>Physical Cores:</b> <code>{}</code>\n<b>Total Cores:</b> <code>{}</code>\n<b>CPU Frequency:</b> <code>{}</code>\n\n<b>Python Version:</b> <code>{}</code>\n<b>Pyrogram Version:</b> <code>{}</code>\n<b>Py-TGcalls Version:</b> <code>{}</code>\n\n<b>Storage Available:</b> <code>{} GB</code>\n<b>Storage Used:</b> <code>{} GB</code>\n<b>Storage Left:</b> <code>{} GB</code>\n\n<b>Served Chats:</b> <code>{}</code>\n<b>Served Users:</b> <code>{}</code>\n<b>Total DB Size:</b> <code>{} MB</code>\n<b>Total DB Storage:</b> <code>{} MB</code>\n<b>Total DB Collections:</b> <code>{}</code>\n<b>Total DB Keys:</b> <code>{}</code>"

    text = m.format(
        len(ALL_MODULES),
        platform.system(),
        ram,
        p_core,
        t_core,
        cpu_freq,
        pyver.split()[0],
        pyrover,
        pytgver,
        str(total)[:4],
        str(used)[:4],
        str(free)[:4],
        served_chats,
        served_users,
        str(datasize)[:6],
        storage,
        call["collections"],
        call["objects"],
    )

    await CallbackQuery.message.reply_text(text=text, reply_markup=upl)
    await CallbackQuery.message.delete()
