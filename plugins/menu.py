import os
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern="^/menu$"))
    async def menu(event):

        base_commands = {
            "/menu": "Show available commands",
            "/alive": "Check bot status",
            "/checkupdate": "Check for updates",
            "/update": "Update the bot",
            "/ping": "Check bot latency",
            "/mode": "Change bot mode",
            "/install": "Install plugins",
            "/reboot": "Restart the bot"
        }

        built_in_plugins = {
            "add": "Add users to group",
            "broadcast": "Broadcast messages to IDs",
            "id": "Get user ID info",
            "insta": "Instagram downloader",
            "mp3": "YouTube to MP3",
            "remove": "Remove installed plugins",
            "yt": "YouTube downloader",
            "checkupdate": "Check bot updates"
        }

        hidden = ["updater_notify.py", "startup.py"]

        plugin_dir = "container_data/user_plugins"
        installed = []

        if os.path.exists(plugin_dir):
            for f in os.listdir(plugin_dir):
                if f.endswith(".py") and f not in hidden:
                    installed.append(f.replace(".py", ""))

        txt = (
            "✦ **X-OPTIMUS COMMAND MENU** ✦\n\n"
            "🌐 **Basic Commands**\n\n"
        )

        for cmd, desc in base_commands.items():
            txt += f"➤ `{cmd}` — {desc}\n"

        txt += "\n🔧 **OTHERS**\n\n"

        for name, desc in built_in_plugins.items():
            txt += f"• `{name}` — {desc}\n"

        txt += "\n📦 **INSTALLED PLUGINS**\n\n"

        if installed:
            for p in installed:
                txt += f"• `{p}`\n"
        else:
            txt += "No plugins installed.\n"

        image_path = "assets/menu.jpg"

        if os.path.exists(image_path):
            await bot.send_file(event.chat_id, image_path, caption=txt)
        else:
            await event.reply(txt)
