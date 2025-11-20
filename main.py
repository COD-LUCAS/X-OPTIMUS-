import os
import importlib
import platform
from dotenv import load_dotenv
from telethon import TelegramClient
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

API_ID = os.getenv("API_ID", "")
API_HASH = os.getenv("API_HASH", "")
STRING = os.getenv("STRING_SESSION", "")
OWNER = os.getenv("OWNER", "Unknown")

if not API_ID or not API_HASH or not STRING:
    print("Missing required credentials")
    exit()

try:
    API_ID = int(API_ID)
except:
    print("API_ID must be integer")
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
                module_path = f"{folder.replace('/', '.')}.{name}"
                try:
                    module = importlib.import_module(module_path)
                    loaded_plugins[name] = module
                    if hasattr(module, "register"):
                        module.register(bot)
                    count += 1
                except Exception as e:
                    print(f"Plugin error {name}: {e}")
    return count

async def start_bot():
    print("══════════════════════")
    print("🚀 X-OPTIMUS STARTING")
    print("══════════════════════")

    total = load_plugins()

    print("🆔 API ID:", API_ID)
    print("👑 Owner:", OWNER)
    print("📦 Plugins Loaded:", total)
    print("💻 Platform:", platform.system())
    print("══════════════════════")

    await bot.start()

    for module in loaded_plugins.values():
        if hasattr(module, "on_startup"):
            try:
                await module.on_startup(bot)
            except:
                pass

    print("🟢 BOT ONLINE & RUNNING")
    print("══════════════════════")

bot.loop.run_until_complete(start_bot())
bot.run_until_disconnected()
