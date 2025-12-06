from telethon import events
import os
import sys

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/reboot$"))
    async def reboot(event):

        uid = event.sender_id

        if uid != bot.owner_id and uid not in bot.sudo_users:
            return await event.reply("❌ Permission denied.")

        await event.reply("🔄 Rebooting…")
        os.execv(sys.executable, [sys.executable] + sys.argv)
