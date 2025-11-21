import os
import time
import platform
from telethon import events, version as telethon_version

START_TIME = time.time()

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/info$"))
    async def info(event):

        me = await bot.get_me()

        owner = os.getenv("OWNER", "Unknown")
        mode = os.getenv("MODE", "private")

        uptime_seconds = int(time.time() - START_TIME)
        uptime = f"{uptime_seconds//3600}h {(uptime_seconds%3600)//60}m"

        txt = (
            "✦ **X-OPTIMUS BOT INFORMATION** ✦\n\n"
            f"🤖 **Bot ID:** `{me.id}`\n"
            f"👤 **Bot Name:** `{me.first_name}`\n"
            f"👑 **Owner:** `{owner}`\n"
            f"🛠 **Developer:** @codlucas\n"
            f"🌐 **Mode:** `{mode}`\n"
            f"📦 **Plugins Loaded:** `{len(bot.list_event_handlers())}`\n"
            f"🕒 **Uptime:** `{uptime}`\n"
            f"💻 **Platform:** `{platform.system()}`\n"
            f"📡 **Telethon Version:** `{telethon_version.__version__}`\n"
        )

        img_path = "assets/info.jpg"

        if os.path.exists(img_path):
            await bot.send_file(event.chat_id, img_path, caption=txt)
        else:
            await event.reply(txt)
