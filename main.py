import os
import sys
import requests
import importlib
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from datetime import datetime

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
STRING = os.environ.get("STRING_SESSION")

bot = TelegramClient(StringSession(STRING), API_ID, API_HASH)
plugins = {}

def load_plugins():
    for filename in os.listdir("plugins"):
        if filename.endswith(".py") and filename != "__init__.py":
            name = filename[:-3]
            try:
                module = importlib.import_module(f"plugins.{name}")
                plugins[name] = module
            except Exception as e:
                print(f"Failed to load {name}: {e}")

load_plugins()

@bot.on(events.NewMessage(pattern=r"\/install (.+)"))
async def install_plugin(event):
    url = event.pattern_match.group(1)
    if not url.startswith("http"):
        return await event.reply("❌ Invalid gist link.")
    try:
        code = requests.get(url).text
        name = "plugin_" + str(len(plugins) + 1)
        with open(f"plugins/{name}.py", "w", encoding="utf-8") as f:
            f.write(code)
        importlib.invalidate_caches()
        module = importlib.import_module(f"plugins.{name}")
        plugins[name] = module
        await event.reply(f"✅ Plugin installed as **{name}**")
    except Exception as e:
        await event.reply(f"❌ Error installing: {e}")

@bot.on(events.NewMessage(pattern=r"\/menu"))
async def menu(event):
    if os.path.exists("assets/menu.jpg"):
        await bot.send_file(event.chat_id, "assets/menu.jpg", caption="📌 **X-OPTIMUS Menu**")
    else:
        await event.reply("Commands:\n/menu\n/ping\n/reboot\n/autoupdate\n/install {gist}")

@bot.on(events.NewMessage(pattern=r"\/ping"))
async def ping(event):
    start = datetime.now()
    msg = await event.reply("Pinging...")
    end = datetime.now()
    ms = (end - start).microseconds // 1000
    if os.path.exists("assets/ping.jpg"):
        await bot.send_file(event.chat_id, "assets/ping.jpg", caption=f"🏓 Pong: **{ms}ms**")
    else:
        await msg.edit(f"🏓 Pong: **{ms}ms**")

@bot.on(events.NewMessage(pattern=r"\/reboot"))
async def reboot(event):
    await event.reply("🔄 Rebooting…")
    os.execv(sys.executable, [sys.executable] + sys.argv)

@bot.on(events.NewMessage(pattern=r"\/autoupdate"))
async def update(event):
    await event.reply("🔄 Updating…")
    os.system("git pull")
    await event.reply("✅ Updated! Restarting…")
    os.execv(sys.executable, [sys.executable] + sys.argv)

print("🚀 X-OPTIMUS USERBOT STARTED...")
bot.start()
bot.run_until_disconnected()
