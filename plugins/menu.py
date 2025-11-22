import os
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/menu$"))
    async def menu(event):

        # MODE CHECK
        if bot.MODE == "PRIVATE" and event.sender_id != bot.owner_id:
            return  # silently block

        # React to command (works on Telethon 1.34+)
        try:
            await event.respond("👍")  # reaction simulation
        except:
            pass

        base_commands = {
            "/menu": "Show available commands",
            "/alive": "Check bot status",
            "/ping": "Check bot latency",
            "/mode": "Change bot mode",
            "/reboot": "Restart the bot",
            "/info": "Bot information",
            "/checkupdate": "Check update",
            "/update": "Update bot",
            "/setvar": "Set ENV variable",
            "/delvar": "Delete ENV variable",
            "/id": "User ID lookup",
            "/uptime": "Show uptime",
            "/install": "Install plugin",
            "/remove": "Remove plugin",
        }

        built_in_plugins = {
            "insta": "Instagram Downloader",
            "yt": "YouTube video downloader",
            "yta": "YouTube audio downloader",
            "mp3": "MP3 converter",
            "img": "Image downloader",
            "genimg": "AI image generator",
            "rbg": "Remove image background",
            "pdf": "Convert images to PDF",
            "url": "Upload media to Catbox"
        }

        hidden = ["updater_notify.py", "startup.py"]
        plugin_dir = "container_data/user_plugins"
        installed = []

        if os.path.exists(plugin_dir):
            for f in os.listdir(plugin_dir):
                if f.endswith(".py") and f not in hidden:
                    installed.append(f.replace(".py", ""))

        # TEXT BLOCK
        txt = (
            "╔══════════════════════════╗\n"
            "║     ⚡ X-OPTIMUS MENU ⚡     ║\n"
            "╚══════════════════════════╝\n\n"
            "🎯 **BASIC COMMANDS**\n"
            "━━━━━━━━━━━━━━━━━━\n"
        )

        for cmd, desc in base_commands.items():
            txt += f"➤ `{cmd}` → {desc}\n"

        txt += (
            "\n🔧 **BUILT-IN FEATURES**\n"
            "━━━━━━━━━━━━━━━━━━\n"
        )

        for name, desc in built_in_plugins.items():
            txt += f"✦ `{name}` → {desc}\n"

        txt += (
            "\n📦 **INSTALLED PLUGINS**\n"
            "━━━━━━━━━━━━━━━━━━\n"
        )

        if installed:
            for p in installed:
                txt += f"⚡ `{p}`\n"
        else:
            txt += "❌ No installed plugins.\n"

        txt += "\n━━━━━━━━━━━━━━━━━━\n"

        # Send menu image if exists
        image_path = "assets/menu.jpg"
        if os.path.exists(image_path):
            await bot.send_file(event.chat_id, image_path, caption=txt)
        else:
            await event.reply(txt)
