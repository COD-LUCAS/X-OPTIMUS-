import os
import importlib
import random
import platform
import time
import asyncio
from dotenv import load_dotenv

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.functions.channels import JoinChannelRequest

# =====================================================================
#  CONFIG LOADER (Supports All Platforms)
# =====================================================================
CONFIG_PATHS = [
    "container_data/config.env",
    "/home/container/container_data/config.env",
    "/home/container/config.env",
    "config.env"
]

loaded = False
for p in CONFIG_PATHS:
    if os.path.exists(p):
        load_dotenv(p)
        loaded = True
        break

if not loaded:
    print("❌ Missing config.env")
    exit()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
STRING = os.getenv("STRING_SESSION")
OWNER = os.getenv("OWNER", "")

if not API_ID or not API_HASH or not STRING:
    print("❌ API_ID / API_HASH / STRING_SESSION missing")
    exit()

API_ID = int(API_ID)

# =====================================================================
#  KEEP ALIVE + AUTO URL FETCH + SELF PING
# =====================================================================
import requests
from threading import Thread
from flask import Flask

app = Flask(__name__)
PUBLIC_URL = None


@app.route("/")
def home():
    return "Bot Alive"


def detect_public_url():
    """
    Auto-detect Render public URL:
    1) Env var
    2) Metadata API (Render)
    3) Domain guess fallback
    """
    global PUBLIC_URL

    # 1) If Render provides it in env
    if os.getenv("RENDER_EXTERNAL_URL"):
        PUBLIC_URL = os.getenv("RENDER_EXTERNAL_URL")
        return PUBLIC_URL

    # 2) Try Metadata API
    try:
        meta = requests.get(
            "http://100.100.100.100/metadata",
            headers={"Metadata-Flavor": "Google"},
            timeout=2
        ).json()

        if "service" in meta and "url" in meta["service"]:
            PUBLIC_URL = meta["service"]["url"]
            return PUBLIC_URL
    except:
        pass

    # 3) Fallback guess
    try:
        name = os.getenv("RENDER_SERVICE_NAME")
        if name:
            PUBLIC_URL = f"https://{name}.onrender.com"
            return PUBLIC_URL
    except:
        pass

    PUBLIC_URL = ""
    return ""


def self_ping():
    """Send request every 4 minutes to avoid Render sleeping."""
    global PUBLIC_URL
    time.sleep(5)

    while True:
        if not PUBLIC_URL:
            detect_public_url()

        if PUBLIC_URL:
            try:
                requests.get(PUBLIC_URL)
                print("🔄 Self Ping →", PUBLIC_URL)
            except:
                print("❌ Self Ping Failed")
        else:
            print("⚠ URL not detected yet")

        time.sleep(240)  # ping every 4 min


def start_keep_alive():
    Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()
    Thread(target=self_ping).start()


# Start anti-sleep system
try:
    start_keep_alive()
    print("⚡ Anti-Sleep KeepAlive System Running")
except Exception as e:
    print("⚠ KeepAlive Failed:", e)

# =====================================================================
#  BOT INITIALIZATION
# =====================================================================
bot = TelegramClient(StringSession(STRING), API_ID, API_HASH)
plugins = {}

REACTIONS = ["👍", "🔥", "😁", "❤️", "👌", "🤝", "🎯", "✨"]


async def auto_react(event):
    try:
        emoji = random.choice(REACTIONS)
        await bot(SendReactionRequest(
            peer=event.chat_id,
            msg_id=event.id,
            reaction=[emoji]
        ))
    except:
        pass


# PATCH EVENT HANDLER
_original_add = bot.add_event_handler


def patched(handler, *args, **kwargs):
    async def wrapper(event):
        if bot.MODE == "PRIVATE" and event.sender_id != bot.owner_id:
            return
        await auto_react(event)
        return await handler(event)

    return _original_add(wrapper, *args, **kwargs)


bot.add_event_handler = patched

# =====================================================================
#  PLUGIN LOADER
# =====================================================================
def load_plugins():
    count = 0
    paths = ["plugins", "container_data/user_plugins"]

    for folder in paths:
        if not os.path.exists(folder):
            continue

        for f in os.listdir(folder):
            if f.endswith(".py") and f != "__init__.py":
                name = f[:-3]
                module_name = f"{folder.replace('/', '.')}.{name}"

                try:
                    module = importlib.import_module(module_name)
                    plugins[name] = module

                    if hasattr(module, "register"):
                        module.register(bot)

                    count += 1
                except Exception as e:
                    print(f"❌ Plugin Error ({name}): {e}")

    return count


# =====================================================================
#  AUTO JOIN CHANNEL
# =====================================================================
async def auto_join():
    try:
        await bot(JoinChannelRequest("xoptimusbothelp"))
    except:
        pass


# =====================================================================
#  START BOT
# =====================================================================
async def start_bot():
    global OWNER

    print("══════════════════════════════")
    print("🚀 X-OPTIMUS STARTING")
    print("══════════════════════════════")

    total = load_plugins()

    print("🆔 API ID:", API_ID)
    print("📦 Plugins Loaded:", total)
    print("💻 Platform:", platform.system())
    print("══════════════════════════════")

    await bot.start()
    bot.START_TIME = time.time()

    me = await bot.get_me()
    if not OWNER:
        OWNER = str(me.id)

    bot.owner_id = int(OWNER)
    bot.MODE = os.getenv("MODE", "PUBLIC").upper()

    await auto_join()

    for m in plugins.values():
        if hasattr(m, "on_startup"):
            try:
                await m.on_startup(bot)
            except:
                pass

    print("🟢 BOT ONLINE")
    print("══════════════════════════════")


# =====================================================================
#  RUN BOT
# =====================================================================
bot.loop.run_until_complete(start_bot())
bot.run_until_disconnected()
