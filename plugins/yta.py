import os
import requests
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/yta(?:\s+(.*))?$"))
    async def yta(event):
        query = event.pattern_match.group(1)

        if not query:
            await event.reply("❌ Give YouTube link!)
            return

        await event.reply("⏳ Downloading audio...")

        try:
            api = f"https://api-aswin-sparky.koyeb.app/api/downloader/song?search={query}"
            r = requests.get(api, timeout=20).json()

            if not r.get("status"):
                await event.reply("❌ Unable to fetch audio.")
                return

            title = r["data"]["title"]
            url = r["data"]["url"]

            temp = f"yta_{event.sender_id}.mp3"

            audio = requests.get(url, stream=True)
            with open(temp, "wb") as f:
                for chunk in audio.iter_content(1024):
                    f.write(chunk)

            await bot.send_file(
                event.chat_id,
                temp,
                caption=f"🎵 **{title}**"
            )

            os.remove(temp)

        except Exception as e:
            await event.reply(f"❌ Error: {e}")
