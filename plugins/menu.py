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

        base = [
            "/ping",
            "/alive",
            "/info",
            "/id",
            "/uptime",
            "/mode",
            "/setvar",
            "/delvar",
            "/checkupdate",
            "/update",
            "/reboot",
            "/list"
        ]

        builtin = [
            "insta",
            "yt",
            "yta",
            "mp3",
            "img",
            "genimg",
            "rbg",
            "pdf",
            "url",
            "chatbot"
        ]

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

        for c in base:
            txt += f"  • `{c}`\n"

        txt += "\n⚙️ **BUILT-IN FEATURES:**\n"
        for n in builtin:
            txt += f"  • `{n}`\n"

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
