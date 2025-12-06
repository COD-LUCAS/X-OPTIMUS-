import os
import requests
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/yta(?:\s+(.*))?$"))
    async def yta(event):

        uid = event.sender_id
        mode = bot.mode.lower()

        if mode == "private":
            if uid != bot.owner_id and uid not in bot.sudo_users:
                return

        query = event.pattern_match.group(1)

        if not query:
            return await event.reply("❌ Give YouTube link!\nExample:\n`/yta https://youtu.be/xxxx`")

        await event.reply("⏳ **Processing your audio...**")

        try:
            api = f"https://api-aswin-sparky.koyeb.app/api/downloader/song?search={query}"
            r = requests.get(api, timeout=20).json()

            if not r.get("status"):
                return await event.reply("❌ Unable to fetch audio from API.")

            title = r["data"]["title"]
            download_url = r["data"]["url"]

            temp_file = f"yta_{event.sender_id}.mp3"

            audio = requests.get(download_url, stream=True)
            with open(temp_file, "wb") as f:
                for chunk in audio.iter_content(4096):
                    if chunk:
                        f.write(chunk)

            await bot.send_file(
                event.chat_id,
                temp_file,
                caption=f"🎵 **{title}**"
            )

            if os.path.exists(temp_file):
                os.remove(temp_file)

        except Exception as e:
            await event.reply(f"❌ Error occurred:\n`{str(e)}`")
