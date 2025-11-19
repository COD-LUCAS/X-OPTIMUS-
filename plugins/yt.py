from telethon import events
import requests
import os

API = "https://api-aswin-sparky.koyeb.app/api/downloader/ytv?url={}"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/yt ?(.*)"))
    async def yt(event):

        url = event.pattern_match.group(1).strip()

        if not url:
            return await event.reply("❗ Send a YouTube link.\nExample: `/yt https://youtu.be/...`")

        # Reaction loading
        try:
            await event.react("⌛")
        except:
            pass

        msg = await event.reply("📥 Downloading video...")

        try:
            res = requests.get(API.format(url)).json()

            if not res.get("status"):
                return await msg.edit("❌ Unable to download this video.")

            info = res["data"]
            video_url = info["url"]
            title = info.get("title", "video")

            safe_title = "".join(c for c in title if c not in "<>:\"/\\|?*")[:50]
            filename = f"{safe_title}.mp4"

            # Download video
            video = requests.get(video_url)

            with open(filename, "wb") as f:
                f.write(video.content)

            await bot.send_file(
                event.chat_id,
                filename,
                caption=f"🎬 **{title}**",
                reply_to=event.id
            )

            os.remove(filename)

            try:
                await event.react("✅")
            except:
                pass

            await msg.delete()

        except Exception as e:
            try:
                await event.react("❌")
            except:
                pass
            await msg.edit(f"❌ Error: {e}")
