import requests
from telethon import events

API = "https://api-aswin-sparky.koyeb.app/api/downloader/song?search="

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/mp3 (.+)"))
    async def yt_mp3(event):
        query = event.pattern_match.group(1).strip()

        msg = await event.reply("🎧 Fetching audio…")

        try:
            # Get audio metadata
            r = requests.get(API + query, timeout=20).json()

            if not r.get("status") or "data" not in r:
                return await msg.edit("❌ Could not find audio.")

            info = r["data"]
            title = info.get("title", "audio")
            audio_url = info.get("url")

            if not audio_url:
                return await msg.edit("❌ No audio URL found.")

            await msg.edit("⚡ Processing…")

            # STREAM DIRECTLY (no file write!)
            stream = requests.get(audio_url, stream=True, timeout=60)
            stream.raise_for_status()

            await bot.send_file(
                event.chat_id,
                stream.raw,   # direct stream to telegram
                file_name=f"{title}.mp3",
                caption=f"🎵 **{title}**",
                force_document=False
            )

            await msg.delete()

        except Exception as e:
            await msg.edit(f"❌ Error:\n`{e}`")
