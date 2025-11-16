from telethon import events
import os

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/menu$"))
    async def menu(event):

        menu_img = "assets/menu.jpg"

        # Load version
        version = "Unknown"
        if os.path.exists("version.txt"):
            with open("version.txt", "r", encoding="utf-8") as f:
                version = f.read().strip()

        # Load mode
        mode = os.environ.get("BOT_MODE", "public").capitalize()

        # Load owner username
        try:
            owner = (await bot.get_me()).username or "Not Set"
        except:
            owner = "Not Set"

        # Get ALL plugins
        plugin_list = []
        for file in os.listdir("plugins"):
            if file.endswith(".py") and file != "__init__.py":
                plugin_list.append(file.replace(".py", ""))

        plugin_list = sorted(plugin_list)

        plugin_text = "\n".join([f"• {name}" for name in plugin_list]) if plugin_list else "No plugins installed."

        caption = (
            "🔱 **X-OPTIMUS PLUGIN MENU**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"🆙 **Version:** {version}\n"
            f"👑 **Owner:** @{owner}\n"
            f"🔧 **Mode:** {mode}\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "**📦 Installed Plugins:**\n"
            f"{plugin_text}"
        )

        # Send image if available
        if os.path.exists(menu_img):
            await event.reply(file=menu_img, caption=caption)
        else:
            await event.reply(caption)
