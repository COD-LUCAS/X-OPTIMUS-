import requests
import os
from telethon import events

API_YT = "https://api-aswin-sparky.koyeb.app/api/downloader/ytv?url="

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/yt (.+)"))
    async def yt(event):
        link = event.pattern_match.group(1).strip()
        msg = await event.reply("⏳ Fetching video info…")

        try:
            r = requests.get(API_YT + link, timeout=40).json()

            if not r.get("status") or "data" not in r:
                return await msg.edit("❌ Unable to fetch video.")

            data = r["data"]
            title = data.get("title", "YouTube Video")
            video_url = data.get("url")

            if not video_url:
                return await msg.edit("❌ No download link found.")

            await msg.edit("⬇️ Downloading video…")

            # ---- DOWNLOAD VIDEO ----
            file_path = "yt_video.mp4"
            with requests.get(video_url, stream=True, timeout=80) as v:
                v.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in v.iter_content(chunk_size=1024 * 512):
                        if chunk:
                            f.write(chunk)

            await msg.edit("📤 Uploading…")

            # ---- SEND VIDEO ----
            await bot.send_file(
                event.chat_id,
                file_path,
                caption=f"🎬 **{title}**",
                supports_streaming=True
            )

            await msg.delete()
            os.remove(file_path)

        except Exception as e:
            await msg.edit(f"❌ Error:\n`{e}`")
            if os.path.exists("yt_video.mp4"):
                os.remove("yt_video.mp4")
