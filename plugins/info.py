import os
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/info$"))
    async def info(event):

        total = len(bot.list_event_handlers())

        txt = (
            "✦ **X-OPTIMUS BOT INFORMATION** ✦\n\n"
            f"🤖 **Bot User:** `{(await bot.get_me()).id}`\n"
            f"👑 **Owner:** `{bot.owner_id}`\n"
            f"🌐 **Mode:** `{bot.MODE}`\n"
            f"📦 **Loaded Plugins:** `{len(bot.list_event_handlers())}`\n"
            f"💻 **Platform:** `{os.name}`\n"
        )

        img_path = "assets/info.jpg"

        if os.path.exists(img_path):
            await bot.send_file(event.chat_id, img_path, caption=txt)
        else:
            await event.reply(txt)
