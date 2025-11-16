from telethon import events
import os
import json
import requests

RAW_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"

CORE = [
    "ping",
    "updater",
    "menu",
    "alive",
    "install",
    "reboot"
]

def local_ver():
    with open("version.json", "r", encoding="utf-8") as f:
        return json.load(f).get("version", "0.0.0")

def remote_ver():
    try:
        r = requests.get(RAW_URL, timeout=5)
        return r.json().get("version", "0.0.0")
    except:
        return "0.0.0"

def parse(v):
    try: return tuple(map(int, v.split(".")))
    except: return (0,)

def register(bot):

    @bot.on(events.NewMessage(pattern="/menu"))
    async def menu(event):
        lv = local_ver()
        rv = remote_ver()

        if parse(rv) > parse(lv):
            status = f"🆕 Update `{lv}` → `{rv}`"
        elif parse(rv) == parse(lv):
            status = f"✅ Up to date `{lv}`"
        else:
            status = f"⚠ Ahead `{lv}`"

        files = os.listdir("plugins")
        installed = sorted([f[:-3] for f in files if f.endswith(".py")])

        core_list = "\n".join(f"• `{c}`" for c in CORE)
        inst_list = "\n".join(f"• `{p}`" for p in installed)

        caption = f"""
🎛 **X-OPTIMUS Control Panel**
━━━━━━━━━━━━━━
📌 Version: `{lv}`
🔄 Status: {status}
━━━━━━━━━━━━━━
🟣 **Core Plugins**
{core_list}

🟢 **Installed Plugins**
{inst_list}

🛠 Commands
/install url name  
/remove name  
/allplug  
/checkupdate  
/update
"""

        await bot.send_file(event.chat_id, "assets/menu.jpg", caption=caption)

    @bot.on(events.NewMessage(pattern="/allplug"))
    async def allplug(event):
        files = os.listdir("plugins")
        plugs = sorted([f[:-3] for f in files if f.endswith(".py")])
        text = "📦 Installed Plugins:\n" + "\n".join(f"• `{p}`" for p in plugs)
        await event.reply(text)

    @bot.on(events.NewMessage(pattern="/remove (.+)"))
    async def remove(event):
        name = event.pattern_match.group(1)
        path = f"plugins/{name}.py"
        if not os.path.exists(path):
            return await event.reply("❌ Not found.")
        os.remove(path)
        await event.reply(f"🗑 Removed `{name}`. Use `/reboot`.")
