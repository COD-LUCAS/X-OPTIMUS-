import requests
import os
from telethon import events

API_YT = "https://api-aswin-sparky.koyeb.app/api/downloader/ytv?url="

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/yt (.+)"))
    async def yt(event):
        link = event.pattern_match.group(1).strip()
        msg = await event.reply("⬇️ Downloading video…")

        try:
            api_url = API_YT + link
            r = requests.get(api_url, timeout=30).json()

            if "data" not in r or not r["data"]:
                return await msg.edit("❌ Unable to download this video.")

            data = r["data"]
            vid_url = data.get("url")
            title = data.get("title", "video")

            if not vid_url:
                return await msg.edit("❌ No downloadable file found.")

            filename = "youtube_video.mp4"

            # Download video
            video = requests.get(vid_url, timeout=60).content
            with open(filename, "wb") as f:
                f.write(video)

            await bot.send_file(
                event.chat_id,
                filename,
                caption=f"🎬 **{title}**"
            )

            await msg.delete()
            os.remove(filename)

        except Exception as e:
            await msg.edit(f"❌ Error:\n`{e}`")
