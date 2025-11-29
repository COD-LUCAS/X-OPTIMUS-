import os
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern="^/menu$"))
    async def menu(event):
        # PRIVATE mode check
        if bot.MODE == "PRIVATE" and event.sender_id != bot.owner_id:
            return

        # Quick reaction
        try:
            await event.react("⚡")
        except:
            pass

        # Scan user plugins
        user_plugins = []
        plugin_dir = "container_data/user_plugins"
        if os.path.exists(plugin_dir):
            user_plugins = [
                f[:-3] for f in os.listdir(plugin_dir) 
                if f.endswith(".py") and not f.startswith("_")
            ]

        # Build menu
        txt = (
            "**⚡ X-OPTIMUS COMMANDS**\n\n"
            "**BASIC:**\n"
            "/ping /alive /info /id /uptime\n"
            "/mode /reboot /setvar /delvar\n"
            "/checkupdate /update\n\n"
            "**FEATURES:**\n"
            "insta yt yta mp3 img genimg\n"
            "rbg pdf url chatbot\n"
        )

        if user_plugins:
            txt += f"\n**PLUGINS ({len(user_plugins)}):**\n"
            # Show in rows of 4
            for i in range(0, len(user_plugins), 4):
                txt += " ".join(user_plugins[i:i+4]) + "\n"
        else:
            txt += "\n**PLUGINS:** None"

        await event.reply(txt, link_preview=False)
