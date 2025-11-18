from telethon import events
import os
import requests
import shutil
import aiohttp
import asyncio

API_URL = "https://api-aswin-sparky.koyeb.app/api/downloader/ytv"
TEMP_FOLDER = "yt_temp"

def register(bot):

    if not os.path.exists(TEMP_FOLDER):
        os.makedirs(TEMP_FOLDER)

    @bot.on(events.NewMessage(pattern=r"^/yt (.+)"))
    async def yt_downloader(event):
        url = event.pattern_match.group(1).strip()

        yt_regex = r"^(https?:\/\/)?(www\.)?(youtube\.com\/(watch\?v=|shorts\/)|youtu\.be\/)"
        if not __import__("re").match(yt_regex, url):
            return await event.reply("❌ Invalid YouTube URL")

        msg = await event.reply("⏳ Fetching video...")

        retry_limit = 3
        data = None

        for attempt in range(retry_limit):
            try:
                response = requests.get(
                    f"{API_URL}?url={url}",
                    verify=False,
                    timeout=40
                )
                data = response.json()
                break
            except Exception:
                if attempt == retry_limit - 1:
                    return await msg.edit("❌ API Error, Try again later.")
                await asyncio.sleep(2)

        if not data or "data" not in data:
            return await msg.edit("❌ Failed to fetch video.")

        video = data["data"]
        title = video.get("title", "YouTube Video")
        download_url = video.get("url")

        if not download_url:
            return await msg.edit("❌ Download URL missing.")

        safe_title = "".join(c for c in title if c.isalnum() or c in " _-")[:50]
        file_path = f"{TEMP_FOLDER}/{safe_title}.mp4"

        await msg.edit("⬇️ Downloading video...")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(download_url, timeout=0) as resp:
                    if resp.status != 200:
                        return await msg.edit("❌ Failed to download video.")

                    with open(file_path, "wb") as f:
                        while True:
                            chunk = await resp.content.read(1024 * 64)
                            if not chunk:
                                break
                            f.write(chunk)
        except Exception as e:
            return await msg.edit(f"❌ Download error: `{e}`")

        if not os.path.exists(file_path):
            return await msg.edit("❌ File not created.")

        await event.reply("🎥 Sending video...", file=file_path)
        await msg.edit("✅ Done!")

        try:
            os.remove(file_path)
        except:
            pass
