import os
import sys
import requests
import importlib
import threading
import uvicorn

from fastapi import FastAPI
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# =============================
# ENV VARIABLES
# =============================

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
STRING = os.environ.get("STRING_SESSION")

# =============================
# WEB SERVER FOR RENDER FREE PLAN
# =============================

app = FastAPI()

@app.get("/")
def home():
    return {"status": "X-OPTIMUS USERBOT ONLINE", "owner": "COD-LUCAS"}

def start_web():
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)

# Start web server in background thread
threading.Thread(target=start_web).start()

# =============================
# TELETHON USERBOT SETUP
# =============================

bot = TelegramClient(StringSession(STRING), API_ID, API_HASH)

# Auto-create plugins folder
if not os.path.exists("plugins"):
    os.makedirs("plugins")

plugins = {}


def load_plugins():
    """Load all plugins inside /plugins folder."""
    for filename in os.listdir("plugins"):
        if filename.endswith(".py"):
            name = filename[:-3]
            try:
                module = importlib.import_module(f"plugins.{name}")
                importlib.reload(module)
                plugins[name] = module

                if hasattr(module, "register"):
                    module.register(bot)

                print(f"🔌 Loaded plugin → {name}")
            except Exception as e:
                print(f"❌ Failed to load {name}: {e}")


load_plugins()

# =============================
# INSTALL PLUGIN
# =============================

@bot.on(events.NewMessage(pattern=r"\/install (.+) (.+)"))
async def install_plugin(event):
    url = event.pattern_match.group(1)
    pname = event.pattern_match.group(2)

    if not url.startswith("http"):
        return await event.reply("❌ Invalid URL.")

    path = f"plugins/{pname}.py"

    if os.path.exists(path):
        return await event.reply("⚠ Plugin already exists. Choose another name.")

    try:
        code = requests.get(url).text
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        importlib.invalidate_caches()
        module = importlib.import_module(f"plugins.{pname}")
        plugins[pname] = module

        if hasattr(module, "register"):
            module.register(bot)

        await event.reply(f"✅ Plugin installed as `{pname}.py`")

    except Exception as e:
        await event.reply(f"❌ Error installing plugin:\n`{e}`")


# =============================
# REBOOT BOT
# =============================

@bot.on(events.NewMessage(pattern=r"\/reboot"))
async def reboot_bot(event):
    await event.reply("🔄 Rebooting…")
    os.execv(sys.executable, [sys.executable] + sys.argv)


# =============================
# AUTO UPDATE BOT
# =============================

@bot.on(events.NewMessage(pattern=r"\/autoupdate"))
async def autoupdate(event):
    await event.reply("♻ Updating from GitHub…")
    os.system("git pull")
    await event.reply("🔄 Restarting after update…")
    os.execv(sys.executable, [sys.executable] + sys.argv)


# =============================
# STARTUP LOG
# =============================

print("🚀 X-OPTIMUS USERBOT IS RUNNING… (Render Free Mode)")


# =============================
# RUN TELETHON
# =============================

bot.start()
bot.run_until_disconnected()
