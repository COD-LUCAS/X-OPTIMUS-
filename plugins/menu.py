from telethon import events
import os
import json
import requests

RAW_VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"

CORE_PLUGINS = [
    "ping",
    "updater",
    "menu",
    "install",
    "reboot"
]

def get_local_version():
    with open("version.json", "r", encoding="utf-8") as f:
        return json.load(f).get("version", "0.0.0")

def get_remote_version():
    try:
        r = requests.get(RAW_VERSION_URL, timeout=5)
        return r.json().get("version", "0.0.0")
    except:
        return "0.0.0"

def parse(v):
    try:
        return tuple(map(int, v.split(".")))
    except:
        return (0,)

def register(bot):

    @bot.on(events.NewMessage(pattern="/menu"))
    async def menu(event):
        local = get_local_version()
        remote = get_remote_version()

        if parse(remote) > parse(local):
            status = f"🆕 Update Available `{local}` → `{remote}`"
        elif parse(remote) == parse(local):
            status = f"✅ Up to Date `{local}`"
        else:
            status = f"⚠ Local Version Ahead `{local}`"

        files = os.listdir("plugins")
        installed = sorted([f[:-3] for f in files if f.endswith(".py")])

        core_list = "\n".join(f"• `{p}`" for p in CORE_PLUGINS)
        installed_list = "\n".join(f"• `{p}`" for p in installed)

        text = f"""
🎛 **X-OPTIMUS Control Panel**
━━━━━━━━━━━━━━━━━━
📦 **Version:** `{local}`
🔄 **Status:** {status}
━━━━━━━━━━━━━━━━━━
🟣 **Core Plugins**
{core_list}

🟢 **Installed Plugins**
{installed_list}

🛠 **Commands**
• `/install url name`
• `/remove name`
• `/allplug`
• `/checkupdate`
• `/update`
"""
        await event.reply(text)

    @bot.on(events.NewMessage(pattern="/allplug"))
    async def allplug(event):
        files = os.listdir("plugins")
        plugs = sorted([f[:-3] for f in files if f.endswith(".py")])
        text = "📦 **Installed Plugins:**\n" + "\n".join(f"• `{p}`" for p in plugs)
        await event.reply(text)

    @bot.on(events.NewMessage(pattern="/remove (.+)"))
    async def remove(event):
        name = event.pattern_match.group(1)
        path = f"plugins/{name}.py"
        if not os.path.exists(path):
            return await event.reply("❌ Plugin not found.")
        os.remove(path)
        await event.reply(f"🗑 Removed `{name}`. Use `/reboot` to apply.")
