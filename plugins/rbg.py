import os
import requests
from telethon import events

CONFIG_KEY = "REMOVE_BG_API_KEY"
CONFIG_FILE = "container_data/config.env"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/rbg$"))
    async def rbg(event):
        api = os.getenv(CONFIG_KEY, "")

        if not api:
            return await event.reply(
                "❌ REMOVE_BG_API_KEY is not set.\n\n"
                "**Set it using:**\n"
                "`/setvar REMOVE_BG_API_KEY=your_api_key_here`"
            )

        if not event.is_reply:
            return await event.reply("Reply to a photo to remove background.")

        reply = await event.get_reply_message
