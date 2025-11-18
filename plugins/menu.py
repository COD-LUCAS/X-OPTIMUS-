import os
from telethon import events

MENU_IMAGE = "assets/menu.jpg"

CORE_COMMANDS = [
    ("menu", "Show available commands"),
    ("alive", "Check bot status"),
    ("checkupdate", "Check for updates"),
    ("update", "Update the bot"),
    ("ping", "Check bot latency"),
    ("mode", "Change bot mode"),
    ("install", "Install plugins"),
    ("reboot", "Restart the bot")
]

EXCLUDE = [
    "menu.py", "alive.py", "updater.py", "ping.py",
    "mode.py", "install.py", "__init__.py",
    "auto_update_notify.py", "startup.py", "reboot.py",
    "sudo.py", "checkupdate.py", "update.py"
]

def scan_folder(folder):
    lst = []
    if os.path.exists(folder):
        for f in os.listdir(folder):
            if f.endswith(".py") and f not in EXCLUDE:
                lst.append(f[:-3])
    return lst

def get_installed_plugins():
    p1 = scan_folder("plugins")
    p2 = scan_folder("plugins/user_plugins")
    final = sorted(set(p1 + p2))
    return final

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/menu$"))
    async def menu(event):

        installed = get_installed_plugins()

        core = "**Basic Commands**\n"
        for cmd, desc in CORE_COMMANDS:
            core += f"/{cmd} - {desc}\n"

        if installed:
            plug = "\n**Installed Plugins**\n"
            for p in installed:
                plug += f"/{p}\n"
        else:
            plug = ""

        text = f"""**Available Commands:**
__________________________________

{core}{plug}
__________________________________

contact @codlucas for any help"""

        try:
            await event.react("📋")
        except:
            pass

        if os.path.exists(MENU_IMAGE):
            await event.reply(file=MENU_IMAGE, message=text)
        else:
            await event.reply(text)
