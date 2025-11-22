import requests
from telethon import events

API_YT = "https://api-aswin-sparky.koyeb.app/api/downloader/ytv?url="

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/yt (.+)"))
    async def yt(event):
        link = event.pattern_match.group(1).strip()

        msg = await event.reply("⏳ Fetching video info…")

        try:
            # ---- RETRY SYSTEM ----
            for i in range(3):
                try:
                    r = requests.get(API_YT + link, timeout=40)
                    data = r.json()
                    break
                except Exception:
                    if i == 2:
                        raise
                    await msg.edit("♻ Retrying…")

            if not data.get("status") or "data" not in data:
                return await msg.edit("❌ API Error. Try again later.")

            info = data["data"]
            title = info.get("title", "YouTube Video")
            video_url = info.get("url")

            if not video_url:
                return await msg.edit("❌ No video link returned.")

            await msg.edit("⚡ Sending video…")

            # ---- FAST DIRECT UPLOAD ----
            await bot.send_file(
                event.chat_id,
                video_url,
                caption=f"🎬 **{title}**",
                supports_streaming=True
            )

            await msg.delete()

        except Exception as e:
            await msg.edit(f"❌ Error:\n`{e}`")
