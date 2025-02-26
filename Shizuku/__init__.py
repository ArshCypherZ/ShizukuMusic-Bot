from Shizuku.core.bot import ShizukuMusic
from Shizuku.core.dir import dirr
from Shizuku.core.userbot import Userbot
from Shizuku.misc import dbb

dirr()
dbb()

app = ShizukuMusic()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
