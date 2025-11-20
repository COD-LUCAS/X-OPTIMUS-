import os
import importlib
import platform
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession

paths = [
    "container_data/config.env",
    "/home/container/container_data/config.env",
    "/home/container_data/config.env"
]

ok = False
for p in paths:
    if os.path.exists(p):
        load_dotenv(p)
        ok = True
        break

if not ok:
    print("Missing config.env")
    exit()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
STRING = os.getenv("STRING_SESSION", "")

if not API_ID or not API_HASH or not STRING:
    print("Missing required credentials")
    exit()

try:
    from webserver import start_webserver
    start_webserver()
except:
    pass

bot = TelegramClient(StringSession(STRING), API_ID, API_HASH)
loaded_plugins = {}

def load_plugins():
    count = 0
    folders = ["plugins", "container_data/user_plugins"]
    for folder in folders:
        if not os.path.exists(folder):
            continue
        for f in os.listdir(folder):
            if f.endswith(".py") and f != "__init__.py":
                name = f[:-3]
                try:
                    module = importlib.import_module(f"{folder.replace('/', '.')}.{name}")
                    loaded_plugins[name] = module
                    if hasattr(module, "register"):
                        module.register(bot)
                    count += 1
                except Exception as e:
                    print("Plugin error:", name, e)
    return count


async def start_bot():
    print("══════════════════════")
    print("🚀 X-OPTIMUS STARTING")
    print("══════════════════════")

    await bot.start()

    me = await bot.get_me()
    bot.owner_id = me.id
    bot.MODE = os.getenv("MODE", "PUBLIC").upper()

    @bot.on(events.NewMessage)
    async def mode_block(event):
        if bot.MODE == "PRIVATE" and event.sender_id != bot.owner_id:
            return

    total = load_plugins()

    for module in loaded_plugins.values():
        if hasattr(module, "on_startup"):
            try:
                await module.on_startup(bot)
            except:
                pass

    print("🆔 API ID:", API_ID)
    print("👑 Owner:", bot.owner_id)
    print("📦 Plugins Loaded:", total)
    print("💻 Platform:", platform.system())
    print("══════════════════════")
    print("🟢 BOT ONLINE & RUNNING")
    print("══════════════════════")

    while True:
        await bot.run_until_disconnected()


bot.loop.run_until_complete(start_bot())
