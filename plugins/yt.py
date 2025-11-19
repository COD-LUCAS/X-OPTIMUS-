from telethon import events
import requests
import os

API = "https://widipe.com/download/ytmp4?url={}"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/yt(?:\s|$)(.*)"))
    async def yt(event):

        url = event.pattern_match.group(1).strip()

        if not url:
            return await event.reply("❗ Send a YouTube link.\nExample: `/yt https://youtu.be/...`")

        try:
            await event.react("⌛")
        except:
            pass

        msg = await event.reply("📥 Downloading video...")

        try:
            r = requests.get(API.format(url)).json()

            if "result" not in r:
                return await msg.edit("❌ API error or unsupported link.")

            video = r["result"]
            title = video.get("title", "video")
            download_url = video.get("url")

            filename = title.replace("/", "_")[:50] + ".mp4"

            file = requests.get(download_url)

            with open(filename, "wb") as f:
                f.write(file.content)

            await bot.send_file(event.chat_id, filename, caption=f"🎬 **{title}**", reply_to=event.id)

            os.remove(filename)

            try:
                await event.react("✅")
            except:
                pass

            await msg.delete()

        except Exception as e:
            await msg.edit(f"❌ Error: {e}")
            try: await event.react("❌")
            except: pass
