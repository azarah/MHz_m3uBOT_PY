import os
import aiohttp

class AmpacheClient:
    def __init__(self):
        self.server = os.getenv("AMPACHE_URL")
        self.token = os.getenv("AMPACHE_TOKEN")

    async def fetch_playlist(self, playlist_id: str):
        """Fetch a playlist using the Ampache token"""
        url = f"{self.server}/server/json.server.php?action=playlist_songs&filter={playlist_id}&auth={self.token}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()

        tracks = []
        for t in data.get("song", []):
            if "url" in t:
                tracks.append(t["url"])
        return tracks
