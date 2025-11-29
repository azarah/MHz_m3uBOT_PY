# MHz_m3uBOT_PY
Python Discord bot that parses and plays M3U playlists.




---

```markdown
# 🎵 MHz_m3uBOT_PY — Discord M3U & Ampache Bot

## Overview

MHz_m3uBOT_PY is a Python Discord bot that allows users to:

- Upload `.m3u` or `.m3u8` playlists directly in Discord.
- Import playlists from Ampache servers.
- View loaded playlists via slash commands.
- **Play playlists in a beautiful web player interface.**
- Operate entirely with **slash commands**, requiring **no privileged intents**.
- Store playlists per user (in-memory cache).

```
```
📂 Folder Structure
MHz_m3uBOT_PY/
│
├── bot.py                 ← Main bot entry point
├── web_server.py           ← Flask web server for web player
├── requirements.txt        ← Python dependencies
├── .env                    ← Bot token and Ampache credentials
├── COMMANDS.md             ← Complete command documentation
│
├── utils/
│   ├── m3u_parser.py      ← M3U parsing logic
│   └── ampache_client.py  ← Ampache API client
│
├── cogs/
│   ├── playlist.py        ← Slash commands (upload/import/view)
│   └── **init**.py        ← Optional, allows clean imports
│
├── templates/
│   └── player.html        ← Web player HTML
│
└── static/
    ├── player.css         ← Web player styles
    └── player.js          ← Web player JavaScript

````

---

## ⚡ Setup Instructions

### 1️⃣ Clone or unzip the project

Place `MHz_m3uBOT_PY` in your working folder.

### 2️⃣ Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
````

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

Dependencies include:

* `discord.py`
* `python-dotenv`
* `aiohttp`
* `flask`
* `flask-cors`

---

### 4️⃣ Configure `.env` file

Copy `.env.example` → `.env` and fill in your credentials:

```dotenv
BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN
GUILD_ID=YOUR_DISCORD_SERVER_ID  # optional for faster slash command sync
AMPACHE_URL=https://your-ampache-server
AMPACHE_USER=bot
AMPACHE_API_KEY=YOUR_LONG_API_KEY
```

---

### 5️⃣ Invite your bot to the server

1. Go to Discord Developer Portal: [https://discord.com/developers/applications](https://discord.com/developers/applications)
2. Select your bot → OAuth2 → URL Generator
3. Select scopes:

   * `bot`
   * `applications.commands`
4. Permissions:

   * Send Messages
   * Embed Links
   * Attach Files
   * Connect & Speak (if future playback is added)
5. Copy the generated URL → open it in a browser → add the bot to your server.

---

### 6️⃣ Run the bot

```bash
python bot.py
```

You should see:

```
Logged in as <bot username>
```

---

## 🛠 Slash Command Usage

### 1️⃣ Upload M3U Playlist

```
/upload_m3u file:<attach your .m3u or .m3u8 file>
```

* Bot parses the file and caches tracks per user.
* Shows first 10 tracks in an embed.

### 2️⃣ View Tracks

```
/tracks
```

* Shows the first 30 tracks of your last uploaded or imported playlist.

### 3️⃣ Import Playlist from Ampache

```
/ampache_import playlist_id:<ID>
```

* Pulls tracks from your Ampache server.
* Stores them in the per-user cache.

### 4️⃣ Get Web Player Token

```
/web_token
```

* Generates a token to access your playlist in the web player.
* Provides a direct link to the web player.
* Use the token at `http://127.0.0.1:5000`

---

## 🌐 Web Player

The bot includes a built-in web player that runs alongside the Discord bot:

* **Access:** `http://127.0.0.1:5000` (default port)
* **Features:**
  - Beautiful, modern UI
  - Play/pause, next/previous controls
  - Progress bar with seeking
  - Volume control
  - Playlist view with track selection
  - Responsive design

**How to use:**
1. Upload or import a playlist using Discord commands
2. Use `/web_token` to get your access token
3. Open the web player URL or enter your token manually
4. Start playing your tracks!

**Note:** The web server starts automatically when the bot runs. You can change the port by setting `WEB_PORT` in your `.env` file.

---

## 💡 Notes

* All slash commands work **without privileged intents**.
* Playlists are cached **per user in memory** — restarting the bot clears them.
* Ampache credentials must be valid and your bot user must have API access.

---

## 🔧 Optional Enhancements

* **Voice playback**: Integrate `discord.FFmpegPCMAudio` to play tracks in voice channels.
* **Persistent storage**: Save playlists to SQLite or MongoDB for permanent caching.
* **Ratings & analytics**: Add commands to rate songs or track usage stats.
* **Ampache favorites export**: Automatically generate M3U playlists from Ampache favorites.

---

## ❌ Troubleshooting

1. **Privileged Intents Error**

   * Already resolved by using **slash commands** only.
   * Ensure your bot code uses only `discord.Intents.default()`.

2. **Bot doesn’t see uploaded files**

   * Make sure you attach `.m3u` or `.m3u8` directly in the slash command.

3. **Ampache Import fails**

   * Check `.env` credentials.
   * Make sure your Ampache user has API access.
   * Verify the playlist ID exists.

---

## 🎉 You’re ready to go!

Your bot can now handle **file uploads**, **Ampache playlist imports**, and display tracks using **slash commands** — all without privileged intents.

```