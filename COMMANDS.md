# 📋 MHz_m3uBOT_PY - Command List

## Overview
This Discord bot allows you to upload, import, and manage M3U playlists directly in Discord using slash commands. All commands work without privileged intents.

---

## 🎵 Available Commands

### `/upload_m3u`
**Description:** Upload and parse an M3U playlist file

**Usage:**
```
/upload_m3u file:<attach your .m3u or .m3u8 file>
```

**Parameters:**
- `file` (required): The `.m3u` or `.m3u8` file to upload

**What it does:**
- Parses the uploaded M3U/M3U8 playlist file
- Extracts all track URLs from the playlist
- Caches the tracks per user (in-memory)
- Displays the first 10 tracks in an embed
- Shows total track count

**Example:**
```
/upload_m3u file:[your_playlist.m3u]
```

**Response:**
- Success: Embed showing "Loaded playlist — X tracks" with first 10 tracks listed
- Error: "File must end with `.m3u` or `.m3u8`" or "No tracks found in playlist"

---

### `/ampache_import`
**Description:** Import playlist from Ampache server by playlist ID

**Usage:**
```
/ampache_import playlist_id:<ID>
```

**Parameters:**
- `playlist_id` (required): The ID of the playlist on your Ampache server

**What it does:**
- Connects to your configured Ampache server
- Fetches the playlist by ID
- Extracts all track URLs from the playlist
- Caches the tracks per user (in-memory)
- Confirms import with track count

**Example:**
```
/ampache_import playlist_id:123
```

**Response:**
- Success: "Imported **X tracks** from Ampache playlist `ID`"
- Error: "No tracks found or invalid playlist ID"

**Requirements:**
- Ampache server must be configured in `.env` file
- Valid `AMPACHE_URL` and `AMPACHE_TOKEN` (or `AMPACHE_API_KEY`) must be set
- The playlist ID must exist on your Ampache server

---

### `/tracks`
**Description:** Display your currently loaded tracks

**Usage:**
```
/tracks
```

**Parameters:** None

**What it does:**
- Retrieves your cached playlist from the bot's memory
- Displays the first 30 tracks in a numbered list
- Shows all tracks if less than 30

**Example:**
```
/tracks
```

**Response:**
- Success: "**Your Playlist:**" followed by numbered list of tracks (up to 30)
- Error: "No playlist loaded" (if you haven't uploaded or imported a playlist yet)

---

### `/web_token`
**Description:** Get your web player access token

**Usage:**
```
/web_token
```

**Parameters:** None

**What it does:**
- Generates a unique access token for the web player
- Provides a direct link to the web player with your token
- Shows how many tracks are available in your playlist

**Example:**
```
/web_token
```

**Response:**
- Success: Embed with your token, web player URL, and track count
- Error: "No playlist loaded" (if you haven't uploaded or imported a playlist yet)

**Note:**
- Token format: `user_id-timestamp`
- Tokens are valid until the bot restarts
- Use the token in the web player at `http://127.0.0.1:5000`

---

## 📝 Notes

### Command Availability
- All commands are **slash commands** (use `/` prefix)
- Commands sync automatically when the bot starts
- No privileged intents required

### Data Storage
- Playlists are cached **per user** in memory
- Each user has their own separate playlist cache
- **Restarting the bot clears all cached playlists**
- To persist playlists, you would need to implement database storage

### File Formats
- Supported formats: `.m3u` and `.m3u8`
- Files must be attached directly in the slash command
- The bot parses standard M3U format (ignores comments starting with `#`)

### Ampache Integration
- Requires valid Ampache server credentials in `.env`
- Uses Ampache JSON API
- Playlist IDs are numeric strings

---

## 🔄 Command Workflow

1. **Upload or Import:**
   - Use `/upload_m3u` to upload a file, OR
   - Use `/ampache_import` to import from Ampache

2. **View Tracks:**
   - Use `/tracks` to see your loaded playlist

3. **Replace Playlist:**
   - Upload or import a new playlist to replace your current one

---

## 🆘 Troubleshooting

### Command not showing up
- Wait a few seconds after bot startup for commands to sync
- Try restarting the bot
- Check that the bot has `applications.commands` scope

### "No playlist loaded"
- Make sure you've used `/upload_m3u` or `/ampache_import` first
- Check that the bot hasn't been restarted (clears cache)

### Ampache import fails
- Verify `.env` has correct `AMPACHE_URL` and `AMPACHE_TOKEN`
- Check that the playlist ID exists on your server
- Ensure your Ampache user has API access

### File upload fails
- Make sure the file ends with `.m3u` or `.m3u8`
- Check that the file is a valid M3U playlist
- Ensure the file is attached directly in the command

