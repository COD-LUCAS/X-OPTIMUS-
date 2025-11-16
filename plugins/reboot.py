from telethon import events
import os
import sys

def register(bot):

    @bot.on(events.NewMessage(pattern=r"\/reboot"))
    async def reboot(event):
        await event.reply("🔄 Rebooting…")
        os.execv(sys.executable, [sys.executable] + sys.argv)
