from telethon import events
import os

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/menu$"))
    async def menu(event):

        img = "assets/menu.jpg"

        # version
        version = "Unknown"
        if os.path.exists("version.txt"):
            version = open("version.txt").read().strip()

        # owner username
        me = await bot.get_me()
        owner = me.username or "COD-LUCAS"

        # mode
        mode = os.environ.get("BOT_MODE", "public").capitalize()

        # list plugins
        plugins = []
        for f in os.listdir("plugins"):
            if f.endswith(".py") and f != "__init__.py":
                plugins.append(f.replace(".py", ""))

        plugins.sort()
        plug_text = "\n".join(f"• {p}" for p in plugins) if plugins else "No plugins installed."

        caption = (
            "🔱 **X-OPTIMUS MENU**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"🆙 **Version:** {version}\n"
            f"👑 **Owner:** @{owner}\n"
            f"🔧 **Mode:** {mode}\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "**📦 Installed Plugins:**\n"
            f"{plug_text}"
        )

        if os.path.exists(img):
            await event.reply(file=img, caption=caption)
        else:
            await event.reply(caption)
