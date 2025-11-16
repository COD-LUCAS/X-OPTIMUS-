from telethon import events
from datetime import datetime
import os

def register(bot):

    @bot.on(events.NewMessage(pattern=r"\/ping"))
    async def ping(event):
        start = datetime.now()
        m = await event.reply("Pinging...")
        end = datetime.now()
        ms = (end - start).microseconds // 1000

        if os.path.exists("assets/ping.jpg"):
            await bot.send_file(event.chat_id, "assets/ping.jpg", caption=f"🫧 Pong: **{ms}ms**")
        else:
            await m.edit(f"🖥️ Pong: **{ms}ms**")
