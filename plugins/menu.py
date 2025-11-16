from telethon import events
import os

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/menu$"))
    async def menu(event):

        img = "assets/menu.jpg"

        version = "Unknown"
        if os.path.exists("version.txt"):
            version = open("version.txt").read().strip()

        owner = "COD-LUCAS"  # FIXED OWNER NAME

        mode = os.environ.get("BOT_MODE", "public").capitalize()

        plugins = []
        for f in os.listdir("plugins"):
            if f.endswith(".py") and f != "__init__.py":
                plugins.append(f[:-3])

        plugins.sort()
        plug_text = "\n".join(f"• {p}" for p in plugins) if plugins else "No plugins installed."

        text = (
            "🔱 **X-OPTIMUS MENU**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"🆙 **Version:** {version}\n"
            f"👑 **Owner:** {owner}\n"
            f"🔧 **Mode:** {mode}\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "**📦 Installed Plugins:**\n"
            f"{plug_text}"
        )

        if os.path.exists(img):
            await event.reply(file=img, message=text)
        else:
            await event.reply(text)
