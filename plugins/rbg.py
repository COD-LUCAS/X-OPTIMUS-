import os
import requests
from telethon import events

CONFIG_KEY = "REMOVE_BG_API_KEY"
CONFIG_FILE = "container_data/config.env"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/rbg$"))
    async def rbg(event):
        api = os.getenv(CONFIG_KEY, "")

        if not api:
            return await event.reply(
                "❌ REMOVE_BG_API_KEY is not set.\n\n"
                "**Set it using:**\n"
                "`/setvar REMOVE_BG_API_KEY=your_api_key_here`"
            )

        if not event.is_reply:
            return await event.reply("Reply to a photo to remove background.")

        reply = await event.get_reply_message()

        if not reply.photo:
            return await event.reply("❌ Reply must be an image.")

        msg = await event.reply("🔄 Removing background...")

        path = await bot.download_media(reply, file="input.png")

        try:
            with open(path, "rb") as f:
                res = requests.post(
                    "https://api.remove.bg/v1.0/removebg",
                    files={"image_file": f},
                    data={"size": "auto"},
                    headers={"X-Api-Key": api},
                    timeout=30
                )

            if res.status_code == 200:
                out = "rbg_done.png"
                with open(out, "wb") as f:
                    f.write(res.content)

                await bot.send_file(event.chat_id, out, caption="✨ Background Removed")
            else:
                await event.reply(f"❌ API error:\n{res.text}")

        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")

        finally:
            if os.path.exists(path):
                os.remove(path)
            if os.path.exists("rbg_done.png"):
                os.remove("rbg_done.png")

        await msg.delete()
