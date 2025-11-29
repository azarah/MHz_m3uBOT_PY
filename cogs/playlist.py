import discord
from discord import app_commands
from discord.ext import commands
from utils.m3u_parser import parse_m3u
from utils.ampache_client import AmpacheClient
import io
import time

class Playlist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cache = {}

    # ---------------------------
    # /upload_m3u with attachment
    # ---------------------------
    @app_commands.command(name="upload_m3u", description="Upload and parse an M3U playlist file")
    @app_commands.describe(file="The .m3u or .m3u8 file to upload")
    async def upload_m3u(self, interaction: discord.Interaction, file: discord.Attachment):
        # Check file extension
        if not (file.filename.endswith(".m3u") or file.filename.endswith(".m3u8")):
            return await interaction.response.send_message("File must end with `.m3u` or `.m3u8`.", ephemeral=True)

        # Read file content
        file_bytes = await file.read()
        content = file_bytes.decode(errors="ignore")

        # Parse playlist
        tracks = parse_m3u(content)
        if not tracks:
            return await interaction.response.send_message("No tracks found in playlist.", ephemeral=True)

        # Cache per user
        self.cache[interaction.user.id] = tracks

        # Show first 10 tracks
        description_lines = [f"{i+1}. {t}" for i, t in enumerate(tracks[:10])]
        if len(tracks) > 10:
            description_lines.append(f"...and {len(tracks)-10} more")

        embed = discord.Embed(
            title=f"Loaded playlist — {len(tracks)} tracks",
            description="\n".join(description_lines),
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(embed=embed)

    # ---------------------------
    # /ampache_import {playlist_id}
    # ---------------------------
    @app_commands.command(name="ampache_import", description="Import playlist from Ampache by ID")
    @app_commands.describe(playlist_id="The ID of the playlist on Ampache")
    async def ampache_import(self, interaction: discord.Interaction, playlist_id: str):
        await interaction.response.defer()
        client = AmpacheClient()
        tracks = await client.fetch_playlist(playlist_id)
        if not tracks:
            await interaction.followup.send("No tracks found or invalid playlist ID.")
            return
        self.cache[interaction.user.id] = tracks
        await interaction.followup.send(f"Imported **{len(tracks)} tracks** from Ampache playlist `{playlist_id}`.")

    # ---------------------------
    # /tracks — show tracks
    # ---------------------------
    @app_commands.command(name="tracks", description="Show your loaded tracks")
    async def tracks(self, interaction: discord.Interaction):
        lst = self.cache.get(interaction.user.id)
        if not lst:
            return await interaction.response.send_message("No playlist loaded.", ephemeral=True)
        text = "\n".join(f"{i+1}. {t}" for i, t in enumerate(lst[:30]))
        await interaction.response.send_message(f"**Your Playlist:**\n{text}")

    # ---------------------------
    # /web_token — get web player token
    # ---------------------------
    @app_commands.command(name="web_token", description="Get your web player access token")
    async def web_token(self, interaction: discord.Interaction):
        lst = self.cache.get(interaction.user.id)
        if not lst:
            return await interaction.response.send_message(
                "No playlist loaded. Upload or import a playlist first.", 
                ephemeral=True
            )
        
        # Generate token: user_id-timestamp
        token = f"{interaction.user.id}-{int(time.time())}"
        web_url = f"http://127.0.0.1:5000/?token={token}"
        
        embed = discord.Embed(
            title="🌐 Web Player Access",
            description=f"Use this token to access your playlist in the web player:",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Token",
            value=f"`{token}`",
            inline=False
        )
        embed.add_field(
            name="Web Player URL",
            value=f"[Click here]({web_url}) or copy the token to the web player",
            inline=False
        )
        embed.add_field(
            name="Tracks",
            value=f"{len(lst)} tracks available",
            inline=False
        )
        embed.set_footer(text="Token expires when bot restarts")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Playlist(bot))
