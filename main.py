import os
import sys
import requests
import importlib
from telethon import TelegramClient, events
from telethon.sessions import StringSession

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
                importlib.reload(module)
                plugins[name] = module
                if hasattr(module, "register"):
                    module.register(bot)
            except Exception as e:
                print(f"Failed to load {name}: {e}")

load_plugins()

@bot.on(events.NewMessage(pattern=r"\/install (.+) (.+)"))
async def install_plugin(event):
    url = event.pattern_match.group(1)
    name = event.pattern_match.group(2)

    if not url.startswith("http"):
        return await event.reply("❌ Invalid link.")

    path = f"plugins/{name}.py"

    if os.path.exists(path):
        return await event.reply("⚠ Plugin name already exists. Choose another.")

    try:
        code = requests.get(url).text
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        importlib.invalidate_caches()
        module = importlib.import_module(f"plugins.{name}")
        plugins[name] = module
        if hasattr(module, "register"):
            module.register(bot)

        await event.reply(f"✅ Plugin installed as `{name}.py`")

    except Exception as e:
        await event.reply(f"❌ Error: {e}")

@bot.on(events.NewMessage(pattern=r"\/reboot"))
async def reboot(event):
    await event.reply("🔄 Rebooting…")
    os.execv(sys.executable, [sys.executable] + sys.argv)

@bot.on(events.NewMessage(pattern=r"\/autoupdate"))
async def autoupdate(event):
    await event.reply("🔄 Updating…")
    os.system("git pull")
    await event.reply("✅ Updated. Restarting…")
    os.execv(sys.executable, [sys.executable] + sys.argv)

print("🚀 X-OPTIMUS USERBOT RUNNING…")
bot.start()
bot.run_until_disconnected()
