from telethon import events
import os
import re

def register(bot):

    @bot.on(events.NewMessage(pattern=r"\/menu"))
    async def menu(event):

        builtin_cmds = [
            "/menu",
            "/ping",
            "/reboot",
            "/autoupdate",
            "/install {gistlink}"
        ]

        plugin_cmds = []

        for filename in os.listdir("plugins"):
            if filename.endswith(".py") and filename not in ["menu.py", "__init__.py"]:
                try:
                    with open(f"plugins/{filename}", "r", encoding="utf-8") as f:
                        content = f.read()

                    patterns = re.findall(r'pattern=r?["\'](.*?)["\']', content)

                    for cmd in patterns:
                        if cmd.startswith(r"\/"):
                            plugin_cmds.append(cmd.replace(r"\/", "/"))

                except Exception:
                    pass

        text = "📌 **X-OPTIMUS Menu**\n\n"

        text += "**🔥 Built-in Commands:**\n"
        for c in builtin_cmds:
            text += f"• `{c}`\n"

        text += "\n**⚙ Installed Plugins:**\n"
        if plugin_cmds:
            for c in plugin_cmds:
                text += f"• `{c}`\n"
        else:
            text += "• No plugins installed\n"

        if os.path.exists("assets/menu.jpg"):
            await bot.send_file(
                event.chat_id,
                "assets/menu.jpg",
                caption=text
            )
        else:
            await event.reply(text)
