import os
from telethon import events
from datetime import datetime

START_IMG = "assets/startup.jpg"

async def register_startup(bot, owner, sudo):
    users = [owner] + sudo
    for uid in users:
        try:
            caption = "🟢 X-OPTIMUS Started Successfully!\nBot is now online and running 🚀"
            if os.path.exists(START_IMG):
                await bot.send_file(uid, START_IMG, caption=caption)
            else:
                await bot.send_message(uid, caption)
        except:
            pass
