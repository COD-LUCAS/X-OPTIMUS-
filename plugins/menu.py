import os
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern="^/menu$"))
    async def menu(event):

        # PRIVATE mode check
        if bot.MODE == "PRIVATE" and event.sender_id != bot.owner_id:
            return

        # REAL TELEGRAM REACTION
        try:
            await event.react("👍")
        except:
            pass

        base = {
            "/ping": "Check bot speed",
            "/alive": "Show alive status",
            "/info": "Bot information",
            "/id": "Get user ID",
            "/uptime": "Show uptime",
            "/mode": "Change public/private",
            "/setvar": "Set ENV variable",
            "/delvar": "Delete ENV variable",
            "/checkupdate": "Check new updates",
            "/update": "Update bot",
            "/reboot": "Restart bot",
        }

        builtin = {
            "insta": "Instagram downloader",
            "yt": "YouTube video",
            "yta": "YouTube audio",
            "mp3": "MP3 converter",
            "img": "Image downloader",
            "genimg": "AI image generator",
            "rbg": "Remove background",
            "pdf": "Convert photos to PDF",
            "url": "Upload media to Catbox",
        }

        user_plugins = []
        plugin_dir = "container_data/user_plugins"
        if os.path.exists(plugin_dir):
            for f in os.listdir(plugin_dir):
                if f.endswith(".py"):
                    user_plugins.append(f.replace(".py", ""))

        txt = (
            " **X-OPTIMUS COMMAND MENU** \n\n"
            "🎯 **BASIC COMMANDS:**\n"
        )

        for c, d in base.items():
            txt += f"  • `{c}` → {d}\n"

        txt += "\n⚙️ **BUILT-IN FEATURES:**\n"
        for n, d in builtin.items():
            txt += f"  • `{n}` → {d}\n"

        txt += "\n📦 **INSTALLED PLUGINS:**\n"
        if user_plugins:
            for p in user_plugins:
                txt += f"  • `{p}`\n"
        else:
            txt += "  • None\n"

        img = "assets/menu.jpg"
        if os.path.exists(img):
            await bot.send_file(event.chat_id, img, caption=txt)
        else:
            await event.reply(txt)
