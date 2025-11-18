from telethon import events
import os
import requests
import shutil
import aiohttp

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

        try:
            api = f"{API_URL}?url={url}"
            res = requests.get(api, verify=False, timeout=10).json()

            if not res.get("status") or "data" not in res:
                return await msg.edit("❌ API error")

            data = res["data"]
            title = data.get("title", "video")
            d_url = data.get("url")

            if not d_url:
                return await msg.edit("❌ Download URL missing")

            safe_title = "".join(c for c in title if c.isalnum() or c in " _-")[:50]
            file_path = f"{TEMP_FOLDER}/{safe_title}.mp4"

            await msg.edit("⬇️ Downloading video...")

            async with aiohttp.ClientSession() as session:
                async with session.get(d_url) as resp:
                    if resp.status != 200:
                        return await msg.edit("❌ Failed to download video")

                    with open(file_path, "wb") as f:
                        while True:
                            chunk = await resp.content.read(1024 * 64)
                            if not chunk:
                                break
                            f.write(chunk)

            if not os.path.exists(file_path) or os.path.getsize(file_path) < 1000:
                return await msg.edit("❌ Corrupted/empty file")

            await event.reply("🎥 Sending video...", file=file_path)

            await msg.edit("✅ Downloaded")

        except Exception as e:
            await msg.edit(f"❌ Error: `{str(e)}`")

        finally:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except:
                pass

            try:
                for f in os.listdir(TEMP_FOLDER):
                    p = f"{TEMP_FOLDER}/{f}"
                    if os.path.isfile(p):
                        if (os.path.getmtime(p) + 600) < __import__("time").time():
                            os.remove(p)
            except:
                pass
