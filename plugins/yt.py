import requests
from telethon import events

API_YT = "https://api-aswin-sparky.koyeb.app/api/downloader/ytv?url="

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/yt (.+)"))
    async def yt(event):
        link = event.pattern_match.group(1).strip()

        status = await event.reply("⏳ **Fetching video info…**")

        try:
            # Get data from API
            api = API_YT + link
            r = requests.get(api, timeout=25).json()

            if not r.get("status") or "data" not in r:
                return await status.edit("❌ **Invalid link or API error.**")

            data = r["data"]
            vid_url = data.get("url")
            title = data.get("title", "YouTube Video")

            if not vid_url:
                return await status.edit("❌ **No video URL found.**")

            await status.edit("⚡ **Processing video…**")

            # STREAM video
            stream = requests.get(vid_url, stream=True, timeout=60)
            if stream.status_code != 200:
                return await status.edit("❌ **Failed to fetch video stream.**")

            await status.edit("⬇️ **Downloading video…**")

            await status.edit("📤 **Uploading to Telegram…**")

            await bot.send_file(
                event.chat_id,
                stream.raw,
                caption=f"🎬 **{title}**",
                force_document=False,
                supports_streaming=True
            )

            await status.edit("✅ **Uploaded Successfully!**")
            await status.delete()

        except Exception as e:
            await status.edit(f"❌ **Error:**\n`{e}`")
