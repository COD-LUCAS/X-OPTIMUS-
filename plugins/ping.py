import os
import time
from datetime import datetime
from telethon import events

PING_IMAGE = "assets/ping.jpg"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/ping$"))
    async def ping(event):
        start = time.perf_counter()
        msg = await event.reply("⌛ Pinging...")
        end = time.perf_counter()

        ping_ms = (end - start) * 1000
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%d/%m/%Y")

        text = f"""
**🚀 X-OPTIMUS IS ALIVE!**

🟣 **Ping:** `{ping_ms:.2f} ms`
🔵 **Time:** `{current_time}`
🟢 **Date:** `{current_date}`
🟡 **Status:** Online
"""

        if os.path.exists(PING_IMAGE):
            await msg.delete()
            await event.reply(file=PING_IMAGE, message=text)
        else:
            await msg.edit(text)
