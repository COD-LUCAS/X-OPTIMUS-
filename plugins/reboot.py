from telethon import events
import os
import sys

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/reboot$"))
    async def reboot(event):

        # OWNER CHECK
        if event.sender_id != bot.owner_id:
            return await event.reply("❌ Only owner can reboot the bot.")

        await event.reply("🔄 Rebooting…")
        os.execv(sys.executable, [sys.executable] + sys.argv)
