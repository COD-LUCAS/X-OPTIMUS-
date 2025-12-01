import os
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern="^/menu$"))
    async def menu(event):

        if bot.MODE == "PRIVATE" and event.sender_id != bot.owner_id:
            return

        try:
            await event.react("👍")
        except:
            pass

        # BASIC
        base = [
            "/ping","/alive","/info","/id","/uptime",
            "/mode","/setvar","/delvar","/checkupdate",
            "/update","/reboot","/list"
        ]

        # BUILT-IN
        builtin = [
            "insta","yt","yta","mp3","img","genimg",
            "rbg","pdf","url","chatbot"
        ]

        # PLUGINS
        plugin_dir = "container_data/user_plugins"
        user_plugins = [
            f.replace(".py","") for f in os.listdir(plugin_dir)
            if f.endswith(".py")
        ] if os.path.exists(plugin_dir) else []

        # TEXT (Ultra fast joining)
        txt = (
            " **X-OPTIMUS COMMAND MENU**\n\n"
            "🎯 **BASIC COMMANDS:**\n"
            f"`{'` `'.join(base)}`\n\n"
            "⚙️ **BUILT-IN FEATURES:**\n"
            f"`{'` `'.join(builtin)}`\n\n"
            "📦 **INSTALLED PLUGINS:**\n"
            f"`{'` `'.join(user_plugins) if user_plugins else 'None'}`"
        )

        img = "assets/menu.jpg"
        if os.path.exists(img):
            await bot.send_file(event.chat_id, img, caption=txt)
        else:
            await event.reply(txt)
