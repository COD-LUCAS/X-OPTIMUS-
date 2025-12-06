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

        uid = event.sender_id
        mode = bot.mode.lower()

        if mode == "private":
            if uid != bot.owner_id and uid not in bot.sudo_users:
                return

        if not hasattr(bot, "START_TIME"):
            bot.START_TIME = time.time()

        sec = int(time.time() - bot.START_TIME)
        uptime_text = format_uptime(sec)

        caption = (
            "╔════ 🔰 **X-OPTIMUS UPTIME** 🔰 ════╗\n"
            f"⏱ **Running:** `{uptime_text}`\n"
            "⚡ **Status:** Stable\n"
            "💠 **Performance:** Excellent\n"
            "╚═════════════════════════════════╝"
        )

        img = "assets/uptime.jpg"

        if os.path.exists(img):
            await bot.send_file(event.chat_id, img, caption=caption)
        else:
            await event.reply(caption)
