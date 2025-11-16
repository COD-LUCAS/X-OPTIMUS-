import os
from telethon import events

MENU_IMAGE = "assets/menu.jpg"  # keep your menu.jpg here

def get_all_commands():
    commands = []
    for file in os.listdir("plugins"):
        if file.endswith(".py") and file != "__init__.py":
            name = file[:-3]
            commands.append(name)
    commands.sort()
    return commands

def register(bot):

    @bot.on(events.NewMessage(pattern="/menu"))
    async def menu(event):

        commands = get_all_commands()
        cmd_list = "\n".join([f"• {cmd}" for cmd in commands])

        text = f"""
🛡️ **X-OPTIMUS COMMAND MENU**

{cmd_list}
"""

        if os.path.exists(MENU_IMAGE):
            await event.reply(
                file=MENU_IMAGE,
                message=text
            )
        else:
            await event.reply(text)
