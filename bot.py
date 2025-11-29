import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import threading
from web_server import run_web_server, set_bot_cache

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", 0))  # Optional: for faster slash command syncing
WEB_PORT = int(os.getenv("WEB_PORT", 5000))  # Web server port

# Only default intents needed (no privileged intents)
intents = discord.Intents.default()

class M3uBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.synced = False

    async def setup_hook(self):
        # Load cogs
        await self.load_extension("cogs.playlist")

    async def on_ready(self):
        if not self.synced:
            if GUILD_ID:  # sync commands to your server immediately
                guild = discord.Object(id=GUILD_ID)
                await self.tree.sync(guild=guild)
            else:
                await self.tree.sync()
            self.synced = True
        print(f"Logged in as {self.user}")
        
        # Start web server in background thread
        self.start_web_server()

    def start_web_server(self):
        """Start the Flask web server in a separate thread"""
        # Get cache reference from playlist cog
        playlist_cog = self.get_cog("Playlist")
        if playlist_cog:
            set_bot_cache(playlist_cog.cache)
            web_thread = threading.Thread(
                target=run_web_server,
                args=('127.0.0.1', WEB_PORT),
                daemon=True
            )
            web_thread.start()
            print(f"Web player started at http://127.0.0.1:{WEB_PORT}")

bot = M3uBot()
bot.run(TOKEN)
