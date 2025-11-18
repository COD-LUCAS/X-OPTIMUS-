import os
import time
from datetime import datetime
from telethon import events

PING_IMAGE = "assets/ping.jpg"

# Moving GIF / MP4 animation URL
PING_GIF = "https://media.tenor.com/On7kvXhzml4AAAAd/loading-gif.gif"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/ping$"))
    async def ping(event):

        # Reaction before ping
        try:
            await event.react("⌛")
        except:
            pass

        start = time.time()

        # Send a moving GIF first
        gif_msg = await event.reply(file=PING_GIF)

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

        # Replace GIF message with final ping result
        if os.path.exists(PING_IMAGE):
            await gif_msg.edit(file=PING_IMAGE, message=text)
        else:
            await gif_msg.edit(text)
