import requests
from telethon import events

API_YT = "https://api-aswin-sparky.koyeb.app/api/downloader/ytv?url="

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/yt (.+)"))
    async def yt(event):
        link = event.pattern_match.group(1).strip()
        msg = await event.reply("⬇️ Fetching video…")

        try:
            # Call your fast API
            r = requests.get(API_YT + link, timeout=30).json()

            if "data" not in r or not r["data"]:
                return await msg.edit("❌ Unable to download this video.")

            data = r["data"]
            vid_url = data.get("url")
            title = data.get("title", "YouTube Video")

            if not vid_url:
                return await msg.edit("❌ Download link not found.")

            await msg.edit("⚡ Downloading at high speed…")

            # STREAMING (no saving to disk)
            with requests.get(vid_url, stream=True, timeout=60) as stream:
                stream.raise_for_status()

                await bot.send_file(
                    event.chat_id,
                    stream.raw,        # send stream directly
                    caption=f"🎬 **{title}**",
                    force_document=False
                )

            await msg.delete()

        except Exception as e:
            await msg.edit(f"❌ Error:\n`{e}`")
