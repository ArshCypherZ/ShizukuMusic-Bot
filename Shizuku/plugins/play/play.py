import random
import string

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message
from pytgcalls.exceptions import NoActiveGroupCall

import config
import logging
from config import lyrical
from Shizuku import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from Shizuku.core.call import ShizukuMusic
from Shizuku.utils import seconds_to_min, time_to_seconds
from Shizuku.utils.channelplay import get_channeplayCB
from Shizuku.utils.decorators.play import PlayWrapper
from Shizuku.utils.formatters import formats
from Shizuku.utils.inline import (
    botplaylist_markup,
    livestream_markup,
    playlist_markup,
    slider_markup,
    track_markup,
)
from Shizuku.utils.stream.stream import stream

play_2 = (
    "<b>Channel Play Mode</b>\n\nProcessing please wait...\n\n<b>Linked Channel:</b> {}"
)
play_1 = "🔎"
play_3 = "Failed to process query."
play_4 = "<b>Admins only playmode</b>\nOnly admins of this chat are allowed to play.\n\nChange it via /playmode"
play_5 = "Failed to process audio file.\n\nAudio file size is very large."
play_6 = "Streams longer than {} are not allowed to play on {}"
play_7 = "Not a valid video file extension.\n\n<b>Supported Extensions:</b> {}"
play_8 = "Video file size should be less than 1 GB"
play_9 = "<b><u>Youtube Playlist Feature</b></u>\n\nSelect the mode in which you want to play whole youtube playlist."
play_10 = "<b>Title:</b> {}\n<b>Duration:</b> {} minutes"
play_11 = "<u><b>{} Spotify Player</b></u>\n\n<b>Requested By:</b> {}"
play_12 = "<u><b>{} Apple Player</b></u>\n\n<b>Requested By:</b> {}"
play_13 = "Live stream detected.\n\nWant me to play it?"
play_14 = "Failed to fetch track details.\n\nTry playing any other"
play_15 = "Failed to process query."
play_16 = "No active voice chat found."
play_17 = "Please turn on voice chat."
play_18 = "<b>Usage:</b> /play [songname/youtube url/reply to audio or video file]"
play_19 = "Queued Playlist:"
play_20 = "Queued Position:"
play_21 = "Added {} tracks to queue.\n\n<b>Check:</b> <a href={}>click here</a>"
play_22 = "Select the playmode: {}"


@app.on_message(
    filters.command(
        [
            "play",
            "vplay",
            "cplay",
            "cvplay",
            "playforce",
            "vplayforce",
            "cplayforce",
            "cvplayforce",
        ]
    )
    & filters.group
)
@PlayWrapper
async def play_commnd(
    client,
    message: Message,
    chat_id,
    video,
    channel,
    playmode,
    url,
    fplay,
):
    mystic = await message.reply_text(play_2.format(channel) if channel else "🔎")
    plist_id = None
    slider = None
    plist_type = None
    spotify = None
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    audio_telegram = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    video_telegram = (
        (message.reply_to_message.video or message.reply_to_message.document)
        if message.reply_to_message
        else None
    )
    if audio_telegram:
        if audio_telegram.file_size > 104857600:
            return await mystic.edit_text(play_5)
        seconds_to_min(audio_telegram.duration)
        if (audio_telegram.duration) > config.DURATION_LIMIT:
            return await mystic.edit_text(
                play_6.format(config.DURATION_LIMIT_MIN, app.mention)
            )
        file_path = await Telegram.get_filepath(audio=audio_telegram)
        if await Telegram.download(message, mystic, file_path):
            message_link = await Telegram.get_link(message)
            file_name = await Telegram.get_filename(audio_telegram, audio=True)
            dur = await Telegram.get_duration(audio_telegram, file_path)
            details = {
                "title": file_name,
                "link": message_link,
                "path": file_path,
                "dur": dur,
            }

            try:
                await stream(
                    mystic,
                    user_id,
                    details,
                    chat_id,
                    user_name,
                    message.chat.id,
                    streamtype="telegram",
                    forceplay=fplay,
                )
            except Exception as e:
                ex_type = type(e).__name__
                err = (
                    e
                    if ex_type == "AssistantErr"
                    else "Something went wrong. Exception: {}".format(ex_type)
                )
                return await mystic.edit_text(err)
            return await mystic.delete()
        return
    elif video_telegram:
        if message.reply_to_message.document:
            try:
                ext = video_telegram.file_name.split(".")[-1]
                if ext.lower() not in formats:
                    return await mystic.edit_text(
                        play_7.format(f"{' | '.join(formats)}")
                    )
            except BaseException:
                return await mystic.edit_text(play_7.format(f"{' | '.join(formats)}"))
        if video_telegram.file_size > config.TG_VIDEO_FILESIZE_LIMIT:
            return await mystic.edit_text(play_8)
        file_path = await Telegram.get_filepath(video=video_telegram)
        if await Telegram.download(message, mystic, file_path):
            message_link = await Telegram.get_link(message)
            file_name = await Telegram.get_filename(video_telegram)
            dur = await Telegram.get_duration(video_telegram, file_path)
            details = {
                "title": file_name,
                "link": message_link,
                "path": file_path,
                "dur": dur,
            }
            try:
                await stream(
                    mystic,
                    user_id,
                    details,
                    chat_id,
                    user_name,
                    message.chat.id,
                    video=True,
                    streamtype="telegram",
                    forceplay=fplay,
                )
            except Exception as e:
                ex_type = type(e).__name__
                err = (
                    e
                    if ex_type == "AssistantErr"
                    else "Some error occured. Exception: {}".format(ex_type)
                )
                return await mystic.edit_text(err)
            return await mystic.delete()
        return
    elif url:
        if await YouTube.exists(url):
            if "playlist" in url:
                try:
                    details = await YouTube.playlist(
                        url,
                        config.PLAYLIST_FETCH_LIMIT,
                        message.from_user.id,
                    )
                except Exception as e:
                    logging.exception(e)
                    return await mystic.edit_text(play_3)
                streamtype = "playlist"
                plist_type = "yt"
                if "&" in url:
                    plist_id = (url.split("=")[1]).split("&")[0]
                else:
                    plist_id = url.split("=")[1]
                cap = play_9
            else:
                try:
                    details, track_id = await YouTube.track(url)
                except Exception as e:
                    logging.exception(e)
                    return await mystic.edit_text(play_3)
                streamtype = "youtube"
                cap = play_10.format(
                    details["title"],
                    details["duration_min"],
                )
        elif await Spotify.valid(url):
            spotify = True
            if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
                return await mystic.edit_text(
                    "Spotify is disabled. Visit support chat."
                )
            if "track" in url:
                try:
                    details, track_id = await Spotify.track(url)
                except Exception as e:
                    logging.exception(e)
                    return await mystic.edit_text(play_3)
                streamtype = "youtube"
                cap = play_10.format(details["title"], details["duration_min"])
            elif "playlist" in url:
                try:
                    details, plist_id = await Spotify.playlist(url)
                except Exception as e:
                    logging.exception(e)
                    return await mystic.edit_text(play_3)
                streamtype = "playlist"
                plist_type = "spplay"
                cap = play_11.format(app.mention, message.from_user.mention)
            elif "album" in url:
                try:
                    details, plist_id = await Spotify.album(url)
                except Exception as e:
                    logging.exception(e)
                    return await mystic.edit_text(play_3)
                streamtype = "playlist"
                plist_type = "spalbum"
                cap = play_11.format(app.mention, message.from_user.mention)
            elif "artist" in url:
                try:
                    details, plist_id = await Spotify.artist(url)
                except Exception as e:
                    logging.exception(e)
                    return await mystic.edit_text(play_3)
                streamtype = "playlist"
                plist_type = "spartist"
                cap = play_11.format(message.from_user.first_name)
            else:
                return await mystic.edit_text(play_15)
        elif await Apple.valid(url):
            if "album" in url:
                try:
                    details, track_id = await Apple.track(url)
                except Exception as e:
                    logging.exception(e)
                    return await mystic.edit_text(play_3)
                streamtype = "youtube"
                cap = play_10.format(details["title"], details["duration_min"])
            elif "playlist" in url:
                spotify = True
                try:
                    details, plist_id = await Apple.playlist(url)
                except Exception as e:
                    logging.exception(e)
                    return await mystic.edit_text(play_3)
                streamtype = "playlist"
                plist_type = "apple"
                cap = play_12.format(app.mention, message.from_user.mention)
            else:
                return await mystic.edit_text(play_3)
        elif await Resso.valid(url):
            try:
                details, track_id = await Resso.track(url)
            except Exception as e:
                    logging.exception(e)
                    return await mystic.edit_text(play_3)
            streamtype = "youtube"
            cap = play_10.format(details["title"], details["duration_min"])
        elif await SoundCloud.valid(url):
            try:
                details, track_path = await SoundCloud.download(url)
            except Exception as e:
                    logging.exception(e)
                    return await mystic.edit_text(play_3)
            duration_sec = details["duration_sec"]
            if duration_sec > config.DURATION_LIMIT:
                return await mystic.edit_text(
                    play_6.format(
                        config.DURATION_LIMIT_MIN,
                        app.mention,
                    )
                )
            try:
                await stream(
                    mystic,
                    user_id,
                    details,
                    chat_id,
                    user_name,
                    message.chat.id,
                    streamtype="soundcloud",
                    forceplay=fplay,
                )
            except Exception as e:
                ex_type = type(e).__name__
                err = (
                    e
                    if ex_type == "AssistantErr"
                    else "Some error occured. Exception: {}".format(ex_type)
                )
                return await mystic.edit_text(err)
            return await mystic.delete()
        else:
            try:
                await ShizukuMusic.stream_call(url)
            except NoActiveGroupCall:
                await mystic.edit_text("Something went wrong.")
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=play_17,
                )
            except Exception as e:
                return await mystic.edit_text("Error occured: {}".format(e))
            await mystic.edit_text("Processing...")
            try:
                await stream(
                    mystic,
                    message.from_user.id,
                    url,
                    chat_id,
                    message.from_user.first_name,
                    message.chat.id,
                    video=video,
                    streamtype="index",
                    forceplay=fplay,
                )
            except Exception as e:
                ex_type = type(e).__name__
                err = e if ex_type == "AssistantErr" else "Oops! Error: {}".format(e)
                return await mystic.edit_text(err)
    else:
        if len(message.command) < 2:
            buttons = botplaylist_markup()
            return await mystic.edit_text(
                play_18,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        slider = True
        query = message.text.split(None, 1)[1]
        if "-v" in query:
            query = query.replace("-v", "")
        try:
            details, track_id = await YouTube.track(query)
        except Exception as e:
            logging.exception(e)
            return await mystic.edit_text(play_3)
        streamtype = "youtube"
    if str(playmode) == "Direct":
        if not plist_type:
            if details["duration_min"]:
                duration_sec = time_to_seconds(details["duration_min"])
                if duration_sec > config.DURATION_LIMIT:
                    return await mystic.edit_text(
                        play_6.format(config.DURATION_LIMIT_MIN, app.mention)
                    )
            else:
                buttons = livestream_markup(
                    track_id,
                    user_id,
                    "v" if video else "a",
                    "c" if channel else "g",
                    "f" if fplay else "d",
                )
                return await mystic.edit_text(
                    play_13,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        try:
            await stream(
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                message.chat.id,
                video=video,
                streamtype=streamtype,
                spotify=spotify,
                forceplay=fplay,
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else "Error: {}".format(e)
            return await mystic.edit_text(err)
        await mystic.delete()
    else:
        if plist_type:
            ran_hash = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=10)
            )
            lyrical[ran_hash] = plist_id
            buttons = playlist_markup(
                ran_hash,
                message.from_user.id,
                plist_type,
                "c" if channel else "g",
                "f" if fplay else "d",
            )
            await mystic.delete()
            await message.reply_text(
                text=cap,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            if slider:
                buttons = slider_markup(
                    track_id,
                    message.from_user.id,
                    query,
                    0,
                    "c" if channel else "g",
                    "f" if fplay else "d",
                )
                await mystic.delete()
                await message.reply_text(
                    text=play_10.format(
                        details["title"].title(),
                        details["duration_min"],
                    ),
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
            else:
                buttons = track_markup(
                    track_id,
                    message.from_user.id,
                    "c" if channel else "g",
                    "f" if fplay else "d",
                )
                await mystic.delete()
                await message.reply_text(
                    text=cap,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )


@app.on_callback_query(filters.regex("MusicStream"))
async def play_music(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    vidid, user_id, mode, cplay, fplay = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer("Not for you.", show_alert=True)
        except BaseException:
            return
    try:
        chat_id, channel = await get_channeplayCB(cplay, CallbackQuery)
    except BaseException:
        return
    user_name = CallbackQuery.from_user.first_name
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except BaseException:
        pass
    mystic = await CallbackQuery.message.reply_text(
        play_2.format(channel) if channel else play_1
    )
    try:
        details, track_id = await YouTube.track(vidid, True)
    except Exception as e:
        logging.exception(e)
        return await mystic.edit_text(play_3)
    if details["duration_min"]:
        duration_sec = time_to_seconds(details["duration_min"])
        if duration_sec > config.DURATION_LIMIT:
            return await mystic.edit_text(
                play_6.format(config.DURATION_LIMIT_MIN, app.mention)
            )
    else:
        buttons = livestream_markup(
            track_id,
            CallbackQuery.from_user.id,
            mode,
            "c" if cplay == "c" else "g",
            "f" if fplay else "d",
        )
        return await mystic.edit_text(
            play_13,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    video = True if mode == "v" else None
    ffplay = True if fplay == "f" else None
    try:
        await stream(
            mystic,
            CallbackQuery.from_user.id,
            details,
            chat_id,
            user_name,
            CallbackQuery.message.chat.id,
            video,
            streamtype="youtube",
            forceplay=ffplay,
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else "Error occured. {}".format(e)
        return await mystic.edit_text(err)
    return await mystic.delete()


@app.on_callback_query(filters.regex("AnonymousAdmin"))
async def anonymous_check(client, CallbackQuery):
    try:
        await CallbackQuery.answer(
            "Revert back to user account:\n\nOpen group settings.\nAdministrators\nClick on your name\nUncheck anonymous admin permissions.",
            show_alert=True,
        )
    except BaseException:
        pass


@app.on_callback_query(filters.regex("ShizukuPlaylists"))
async def play_playlists_command(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    (
        videoid,
        user_id,
        ptype,
        mode,
        cplay,
        fplay,
    ) = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer("not for you", show_alert=True)
        except BaseException:
            return
    try:
        chat_id, channel = await get_channeplayCB(cplay, CallbackQuery)
    except BaseException:
        return
    user_name = CallbackQuery.from_user.first_name
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except BaseException:
        pass
    mystic = await CallbackQuery.message.reply_text(
        play_2.format(channel) if channel else play_1
    )
    videoid = lyrical.get(videoid)
    video = True if mode == "v" else None
    ffplay = True if fplay == "f" else None
    spotify = True
    if ptype == "yt":
        spotify = False
        try:
            result = await YouTube.playlist(
                videoid,
                config.PLAYLIST_FETCH_LIMIT,
                CallbackQuery.from_user.id,
                True,
            )
        except Exception as e:
            logging.exception(e)
            return await mystic.edit_text(play_3)
    if ptype == "spplay":
        try:
            result, spotify_id = await Spotify.playlist(videoid)
        except Exception as e:
            logging.exception(e)
            return await mystic.edit_text(play_3)
    if ptype == "spalbum":
        try:
            result, spotify_id = await Spotify.album(videoid)
        except Exception as e:
            logging.exception(e)
            return await mystic.edit_text(play_3)
    if ptype == "spartist":
        try:
            result, spotify_id = await Spotify.artist(videoid)
        except Exception as e:
            logging.exception(e)
            return await mystic.edit_text(play_3)
    if ptype == "apple":
        try:
            result, apple_id = await Apple.playlist(videoid, True)
        except Exception as e:
            logging.exception(e)
            return await mystic.edit_text(play_3)
    try:
        await stream(
            mystic,
            user_id,
            result,
            chat_id,
            user_name,
            CallbackQuery.message.chat.id,
            video,
            streamtype="playlist",
            spotify=spotify,
            forceplay=ffplay,
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else "Error occured. {}".format(e)
        return await mystic.edit_text(err)
    return await mystic.delete()


@app.on_callback_query(filters.regex("slider"))
async def slider_queries(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    (
        what,
        rtype,
        query,
        user_id,
        cplay,
        fplay,
    ) = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer("Not for you.", show_alert=True)
        except BaseException:
            return
    what = str(what)
    rtype = int(rtype)
    if what == "F":
        if rtype == 9:
            query_type = 0
        else:
            query_type = int(rtype + 1)
        try:
            await CallbackQuery.answer("Please wait.")
        except BaseException:
            pass
        title, duration_min, vidid = await YouTube.slider(query, query_type)
        buttons = slider_markup(vidid, user_id, query, query_type, cplay, fplay)
        return await CallbackQuery.edit_message_text(
            text=play_10.format(title.title(), duration_min),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if what == "B":
        if rtype == 0:
            query_type = 9
        else:
            query_type = int(rtype - 1)
        try:
            await CallbackQuery.answer("Please wait.")
        except BaseException:
            pass
        title, duration_min, vidid = await YouTube.slider(query, query_type)
        buttons = slider_markup(vidid, user_id, query, query_type, cplay, fplay)
        return await CallbackQuery.edit_message_text(
            text=play_10.format(title.title(), duration_min),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
