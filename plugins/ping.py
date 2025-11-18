import os
import time
from datetime import datetime
from telethon import events

PING_IMAGE = "assets/ping.jpg"
PING_GIF = "https://i.gifer.com/YCZH.gif"  # Animated hourglass GIF

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/ping$"))
    async def ping(event):

        start = time.time()

        # Send animated hourglass GIF
        loading = await event.reply(file=PING_GIF)

        end = time.time()
        ping_time = (end - start) * 1000

        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%d/%m/%Y")

        text = f"""
**🚀 X-OPTIMUS IS ALIVE!**

🟣 **Ping:** `{ping_time:.2f}ms`
🔵 **Time:** `{current_time}`
🟢 **Date:** `{current_date}`
🟡 **Status:** Online

✨ *Bot is running smoothly!* ✨
"""

        # Replace GIF with final ping message + image if available
        if os.path.exists(PING_IMAGE):
            await loading.edit(file=PING_IMAGE, message=text)
        else:
            await loading.edit(text)
