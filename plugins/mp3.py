import requests
from telethon import events
from io import BytesIO

API = "https://api-aswin-sparky.koyeb.app/api/downloader/song?search="

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/mp3 (.+)"))
    async def yt_mp3(event):
        query = event.pattern_match.group(1).strip()

        msg = await event.reply("🎧 Fetching audio…")

        try:
            r = requests.get(API + query, timeout=20).json()

            if not r.get("status") or "data" not in r:
                return await msg.edit("❌ Could not find audio.")

            info = r["data"]
            title = info.get("title", "audio")
            audio_url = info.get("url")

            if not audio_url:
                return await msg.edit("❌ No audio URL found.")

            await msg.edit("⬇️ Downloading audio…")

            # Download FAST into memory
            dl = requests.get(audio_url, timeout=50)
            dl.raise_for_status()

            audio_bytes = BytesIO(dl.content)
            audio_bytes.name = f"{title}.mp3"

            await bot.send_file(
                event.chat_id,
                audio_bytes,
                caption=f"🎵 **{title}**",
                force_document=False
            )

            await msg.delete()

        except Exception as e:
            await msg.edit(f"❌ Error:\n`{e}`")
