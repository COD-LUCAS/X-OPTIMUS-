import os
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/menu$"))
    async def menu(event):

        img = "assets/menu.jpg"

        # version from version.txt
        version = "Unknown"
        if os.path.exists("version.txt"):
            version = open("version.txt").read().strip()

        # owner from config.env
        owner = os.getenv("OWNER", "Unknown")

        # get all plugins
        files = []
        for f in os.listdir("plugins"):
            if f.endswith(".py") and f != "__init__.py":
                files.append(f[:-3])

        files.sort()
        plist = "\n".join(f"• {p}" for p in files) if files else "No plugins found."

        text = (
            "🔱 **X-OPTIMUS MENU**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"🆙 Version: `{version}`\n"
            f"👑 Owner: `{owner}`\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "**📦 Installed Plugins:**\n"
            f"{plist}"
        )

        if os.path.exists(img):
            await bot.send_file(event.chat_id, img, caption=text)
        else:
            await event.reply(text)
