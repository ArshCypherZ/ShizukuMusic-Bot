# Shizuku - Telegram Music Bot 🎶

[![GitHub Stars](https://img.shields.io/github/stars/ArshCypherZ/ShizukuMusic-Bot?style=for-the-badge)](https://github.com/ArshCypherZ/ShizukuMusic-Bot/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/ArshCypherZ/ShizukuMusic-Bot?style=for-the-badge)](https://github.com/ArshCypherZ/ShizukuMusic-Bot/network)
[![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Telegram Support](https://img.shields.io/badge/Support-Telegram-blue?style=for-the-badge)](https://t.me/SpiralTechDivision)

A high-performance Telegram music bot that combines multiple streaming sources with enterprise-grade features. Bypass regional restrictions and enjoy seamless music playback directly in your Telegram groups.

## Table of Contents
- [Features](#features-)
- [Installation](#installation-)
  - [Prerequisites](#prerequisites)
  - [Traditional Setup](#traditional-setup)
  - [Docker Setup](#docker-setup-)
- [Configuration](#configuration-)
- [Usage](#usage-)
- [Deployment](#deployment-)
- [Contributing](#contributing-)
- [Credits](#credits-)
- [License](#license-)
- [Support](#support-)

## Features ✨
- 🚫 **YouTube Ban Bypass**: Leverage alternative methods to stream when YouTube is blocked
- 🎧 **Multi-Source Streaming**: Supports YouTube, Spotify (tracks/albums/playlists)
- 🐳 **Docker First**: Ready-to-use container images with auto-update support
- 🔧 **Advanced Controls**:
  - Audio quality selection
  - Persistent queue system with save/load functionality
- 🌙 **24/7 Mode**: Background worker keeps music playing continuously
- 🔒 **Role-Based Access**: Granular permissions for admins/moderators

## Installation ⚙️

### Prerequisites
- Python 3.9+
- FFmpeg
- Telegram API ID & Hash ([my.telegram.org](https://my.telegram.org))
- Spotify Client ID & Secret ([developer.spotify.com](https://developer.spotify.com)) (Optional)
- MongoDB URL

### Traditional Setup
```bash
git clone https://github.com/ArshCypherZ/ShizukuMusic-Bot.git
cd ShizukuMusic-Bot

apt-get -y update && apt-get -y install git gcc python3-dev ffmpeg zip

# Install dependencies
pip3 install -U -r requirements.txt
```

Generate cookies of youtube.com using cookies.txt extension on your browser and replace with youtube.txt

# Start the bot
```bash
python3 -m Shizuku
```

### Docker Setup 🐳
You can build and run with Dockerfile or setup containers with docker-compose.yml. Checkout docker's documentation for more.

## Configuration ⚙️
Edit `config.py` file with mandatory variables.

## Usage 🎮
| Command                | Description                          | Example                      |
|------------------------|--------------------------------------|------------------------------|
| `/play [query]`        | Play from any supported source       | `/play Hotel California`     |
| `/play [spotify url]`  | Direct Spotify link playback         | `/splay spotify:track:12345` |
| `/vplay [query/url]`   | Video playback from any source       | `/splay spotify:track:12345` |
| `/queue`               | Show current queue with progress bar | `/queue`                     |
| `/loop [on/off]`       | Toggle track looping                 | `/loop on`                   |
| `/help`                | Lists all available commands         | `/help`                      |

## Deployment 🚀
For production deployment, consider:
1. **Process Manager**: Use systemd or pm2 for auto-restart
   ```bash
   # systemd example
   sudo nano /etc/systemd/system/shizuku.service
   ```
2. **Reverse Proxy**: Nginx for SSL termination
3. **Monitoring**: Health checks at `/ping` command inside bot.

## Contributing 🤝
We welcome contributions! Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Credits 🙏
- Core Framework: Kurigram (Fork of [Pyrogram](https://github.com/pyrogram/pyrogram))
- Audio Engine: [FFmpeg](https://ffmpeg.org) & [PyTgCalls](https://github.com/pytgcalls/pytgcalls)
- Inspired by [Yukki Music Bot](https://github.com/TeamYukki/YukkiMusicBot)

## License 📄
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 💬
For assistance, join our [Telegram Support Group](https://t.me/SpiralTechDivision) or open a [GitHub Issue](https://github.com/ArshCypherZ/ShizukuMusic-Bot/issues).

---

**Enjoy limitless music with Shizuku!** 🎧🚀