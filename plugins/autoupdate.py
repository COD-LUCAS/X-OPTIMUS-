from telethon import events
import os
import sys

def register(bot):

    @bot.on(events.NewMessage(pattern=r"\/autoupdate"))
    async def auto(event):
        await event.reply("🔄 Updating from GitHub…")
        os.system("git pull")
        await event.reply("✅ Updated! Restarting…")
        os.execv(sys.executable, [sys.executable] + sys.argv)
