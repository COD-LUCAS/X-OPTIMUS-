import os
import importlib
import platform
import time
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import SendReactionRequest
import random

CONFIGS = [
    "container_data/config.env",
    "/home/container/container_data/config.env",
    "/home/container/config.env"
]

loaded = False
for c in CONFIGS:
    if os.path.exists(c):
        load_dotenv(c)
        loaded = True
        break

if not loaded:
    print("Missing config.env")
    exit()

API_ID = os.getenv("API_ID", "")
API_HASH = os.getenv("API_HASH", "")
STRING = os.getenv("STRING_SESSION", "")
OWNER = os.getenv("OWNER", "")

if not API_ID or not API_HASH or not STRING:
    print("Missing API_ID/API_HASH/STRING_SESSION")
    exit()

API_ID = int(API_ID)

try:
    from webserver import start_webserver
    start_webserver()
except:
    pass

bot = TelegramClient(StringSession(STRING), API_ID, API_HASH)
plugins = {}

REACTIONS = ["👍", "🔥", "😁", "❤️", "👌", "🤝", "🎯", "✨"]

async def auto_react(event, bot):
    try:
        emoji = random.choice(REACTIONS)
        await bot(SendReactionRequest(
            peer=event.chat_id,
            msg_id=event.id,
            reaction=[emoji]
        ))
    except:
        pass

original_add_event = bot.add_event_handler

def patched(handler, *args, **kwargs):
    async def wrapper(event):
        if bot.MODE == "PRIVATE" and event.sender_id != bot.owner_id:
            return
        await auto_react(event, bot)
        return await handler(event)
    return original_add_event(wrapper, *args, **kwargs)

bot.add_event_handler = patched

def load_plugins():
    count = 0
    paths = ["plugins", "container_data/user_plugins"]
    for folder in paths:
        if not os.path.exists(folder):
            continue
        for f in os.listdir(folder):
            if f.endswith(".py") and f != "__init__.py":
                name = f[:-3]
                module_path = f"{folder.replace('/', '.')}.{name}"
                try:
                    module = importlib.import_module(module_path)
                    plugins[name] = module
                    if hasattr(module, "register"):
                        module.register(bot)
                    count += 1
                except Exception as e:
                    print(f"Plugin error in {name}: {e}")
    return count

async def auto_join_channel():
    try:
        await bot(JoinChannelRequest("xoptimusbothelp"))
    except:
        pass

async def start_bot():
    global OWNER
    print("══════════════════════")
    print("🚀 X-OPTIMUS STARTING")
    print("══════════════════════")

    total = load_plugins()

    print("🆔 API ID:", API_ID)
    print("👑 Owner:", OWNER if OWNER else "Auto")
    print("📦 Plugins Loaded:", total)
    print("💻 Platform:", platform.system())
    print("══════════════════════")

    await bot.start()
    bot.START_TIME = time.time()

    me = await bot.get_me()
    if not OWNER:
        OWNER = str(me.id)
    bot.owner_id = int(OWNER)

    bot.MODE = os.getenv("MODE", "PUBLIC").upper()

    await auto_join_channel()

    for m in plugins.values():
        if hasattr(m, "on_startup"):
            try:
                await m.on_startup(bot)
            except:
                pass

    print("🟢 BOT ONLINE & RUNNING")
    print("══════════════════════")

bot.loop.run_until_complete(start_bot())
bot.run_until_disconnected()
