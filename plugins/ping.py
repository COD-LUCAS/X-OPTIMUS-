import os
import time
from datetime import datetime
from telethon import events

PING_IMAGE = "assets/ping.jpg"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/ping$"))
    async def ping(event):

        start = time.time()
        reply = await event.reply("❤️ Pinging...")
        end = time.time()

        ping_ms = (end - start) * 1000

        time_now = datetime.now().strftime("%H:%M:%S")
        date_now = datetime.now().strftime("%d/%m/%Y")

        text = f"""
**🚀 X-OPTIMUS IS ALIVE!**

🟣 **Ping:** `{ping_ms:.2f}ms`
🔵 **Time:** `{time_now}`
🟢 **Date:** `{date_now}`
🟡 **Status:** Online

✨ *Bot is running smoothly!* ✨
"""

        if os.path.exists(PING_IMAGE):
            await reply.edit(file=PING_IMAGE, message=text)
        else:
            await reply.edit(text)
