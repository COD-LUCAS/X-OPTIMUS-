import os
import time
from telethon import events

def format_uptime(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    return f"{d}d {h}h {m}m {s}s"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/uptime$"))
    async def uptime(event):

        sec = int(time.time() - bot.START_TIME)
        uptime_text = format_uptime(sec)

        caption = (
            "━━━━━━━━━━━━━━━━\n"
            "🕒 **X-OPTIMUS UPTIME**\n"
            "━━━━━━━━━━━━━━━━\n"
            f"⏱ **Running:** `{uptime_text}`\n"
            "⚡ **Performance:** Excellent\n"
            "━━━━━━━━━━━━━━━━"
        )

        img = "assets/uptime.jpg"

        if os.path.exists(img):
            await bot.send_file(event.chat_id, img, caption=caption)
        else:
            await event.reply(caption)
