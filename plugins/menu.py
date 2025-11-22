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
            "/checkupdate": "Check bot updates",
            "/ping": "Check bot latency",
            "/mode": "Change bot mode",
            "/install": "Install plugins",
            "/remove": "Remove installed plugins",
            "/reboot": "Restart the bot",
            "/info": "Get info of the bot",
            "/setvar": "set variable in your bot",
            "/delvar": "delete variable",
            "/id": "Get user ID info",
            "/uptime": "uptime stats"
        }

        built_in_plugins = {
            "insta": "Instagram downloader",
            "mp3": "To MP3",
            "yta": "youtube audio downloader",
            "yt": "YouTube video downloader",
           "rbg": "remove background of photo",
            "img": "download images",
            "pdf" : "make pages to pdf",
            "genimg" : "generate images using AI",
            "url": "Uploads media to Catbox"
            
        }

        hidden = ["updater_notify.py", "startup.py"]

        plugin_dir = "container_data/user_plugins"
        installed = []

        if os.path.exists(plugin_dir):
            for f in os.listdir(plugin_dir):
                if f.endswith(".py") and f not in hidden:
                    installed.append(f.replace(".py", ""))

        txt = (
            "╔═══════════════════════════╗\n"
            "║   𝗫-𝗢𝗣𝗧𝗜𝗠𝗨𝗦 𝗖𝗢𝗠𝗠𝗔𝗡𝗗 𝗠𝗘𝗡𝗨   ║\n"
            "╚═══════════════════════════╝\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🎯 𝗕𝗔𝗦𝗜𝗖 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        )

        for cmd, desc in base_commands.items():
            txt += f"▸ `{cmd}` ➜ {desc}\n"

        txt += (
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🔧 𝗢𝗧𝗛𝗘𝗥 𝗙𝗘𝗔𝗧𝗨𝗥𝗘𝗦\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        )

        for name, desc in built_in_plugins.items():
            txt += f"◈ `{name}` ➜ {desc}\n"

        txt += (
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📦 𝗜𝗡𝗦𝗧𝗔𝗟𝗟𝗘𝗗 𝗣𝗟𝗨𝗚𝗜𝗡𝗦\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        )

        if installed:
            for p in installed:
                txt += f"⚡ `{p}`\n"
        else:
            txt += "❌ 𝘕𝘰 𝘱𝘭𝘶𝘨𝘪𝘯𝘴 𝘪𝘯𝘴𝘵𝘢𝘭𝘭𝘦𝘥.\n"

        txt += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

        image_path = "assets/menu.jpg"

        if os.path.exists(image_path):
            await bot.send_file(event.chat_id, image_path, caption=txt)
        else:
            await event.reply(txt)
            
