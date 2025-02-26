HELP_1 = """Admin Commands:

Just add 'c' in the starting of the commands to use them for channel.

/pause: Pause the current playing stream.
/resume: Resume the paused stream.
/skip: Skip the current playing stream and start streaming the next track in queue.
/end or /stop: Clears the queue and ends the current playing stream.
/player: Get an interactive player panel.
/queue: Shows the queued tracks list.
"""

HELP_2 = """Auth Users:

Auth users can use admin rights in the bot without admin rights in the chat.

/auth [username/user_id]: Add a user to auth list of the bot.
/unauth [username/user_id]: Remove a user from the auth users list.
/authusers: Shows the list of auth users of the group.
"""

HELP_3 = """Broadcast Feature:

/broadcast [message or reply to a message]: Broadcast a message to served chats of the bot.

Broadcasting Modes:
-pin: Pins your broadcasted messages in served chats.
-pinloud: Pins your broadcasted message in served chats and sends notification to the members.
-user: Broadcasts the message to the users who have started your bot.
-assistant: Broadcast your message from the assistant account of the bot.
-nobot: Forces the bot to not broadcast the message.

Example: /broadcast -user -assistant -pin Testing Broadcast
"""

HELP_4 = """Chat Blacklist Feature:

Restrict shit chats to use our precious bot.

/blacklistchat [chat_id]: Blacklist a chat from using the bot.
/whitelistchat [chat_id]: Whitelist the blacklisted chat.
/blacklistedchat: Shows the list of blacklisted chats.
"""

HELP_5 = """Block Users:

Starts ignoring the blacklisted user, so that he can't use bot commands.

/block [username or reply to a user]: Block the user from our bot.
/unblock [username or reply to a user]: Unblocks the blocked user.
/blockedusers: Shows the list of blocked users.
"""

HELP_6 = """Channel Play Commands:

You can stream audio/video in channels.

/cplay: Starts streaming the requested audio track on the channel's video chat.
/cvplay: Starts streaming the requested video track on the channel's video chat.
/cplayforce or /cvplayforce: Stops the ongoing stream and starts streaming the requested track.
/channelplay [chat username or id] or [disable]: Connect channel to a group and starts streaming tracks by the help of commands sent in group.
"""

HELP_7 = """Global Ban Feature:

/gban [username or reply to a user]: Globally bans the chutiya from all the served chats and blacklists him from using the bot.
/ungban [username or reply to a user]: Globally unbans the globally banned user.
/gbannedusers: Shows the list of globally banned users.
"""

HELP_8 = """Loop Stream:

Starts streaming the ongoing stream in loop.

/loop [enable/disable]: Enables/Disables loop for the ongoing stream.
/loop [1, 2, 3, ...]: Enables the loop for the given value.
"""

HELP_9 = """Maintenance Mode:

/logs: Get logs of the bot.
/logger [enable/disable]: Bot will start logging the activities happening on bot.
/maintenance [enable/disable]: Enable or disable the maintenance mode of your bot.
"""

HELP_10 = """Ping & Stats:

/start: Starts the music bot.
/help: Get help menu with explanation of commands.

/ping: Shows the ping and system stats of the bot.
/stats: Shows the overall stats of the bot.
"""

HELP_11 = """Play Commands:

v: Stands for video play.
force: Stands for force play.

/play or /vplay: Starts streaming the requested track on video chat.
/playforce or /vplayforce: Stops the ongoing stream and starts streaming the requested track.
"""

HELP_12 = """Shuffle Queue:

/shuffle: Shuffles the queue.
/queue: Shows the shuffled queue.
"""

HELP_13 = """Seek Stream:

/seek [duration in seconds]: Seeks the stream to the given duration.
/seekback [duration in seconds]: Backward seek the stream to the the given duration.
"""

HELP_14 = """Song Download:

/song [song name/yt URL]: Download any track from YouTube in mp3 or mp4 formats.
"""

HELP_15 = """Speed Commands:

You can control the playback speed of the ongoing stream. [Admins only]

/speed or /playback: For adjusting the audio playback speed in group.
/cspeed or /cplayback: For adjusting the audio playback speed in channel.
"""
