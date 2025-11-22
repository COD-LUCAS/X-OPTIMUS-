import requests
from telethon import events

API_YT = "https://api-aswin-sparky.koyeb.app/api/downloader/ytv?url="

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/yt (.+)"))
    async def yt(event):
        url = event.pattern_match.group(1).strip()

        status = await event.reply("⏳ Fetching info…")

        try:
            data = requests.get(API_YT + url, timeout=15).json()
            if not data.get("status") or "data" not in data:
                return await status.edit("❌ API error or invalid link.")

            info = data["data"]
            video_url = info.get("url")
            title = info.get("title", "YouTube Video")

            if not video_url:
                return await status.edit("❌ No video URL found.")

            await status.edit("⚡ Sending video…")

            # 💥 DIRECT LINK UPLOAD (SUPER FAST)
            await bot.send_file(
                event.chat_id,
                video_url,
                caption=f"🎬 **{title}**",
                supports_streaming=True
            )

            await status.delete()

        except Exception as e:
            await status.edit(f"❌ Error:\n`{e}`")
