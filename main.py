import os
import importlib
import platform
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

paths = [
    "/home/container/container_data/config.env",
    "/home/container_data/config.env",
    "container_data/config.env"
]

config_loaded = False
for p in paths:
    if os.path.exists(p):
        load_dotenv(p)
        config_loaded = True
        break

if not config_loaded:
    print("❌ Missing config.env")
    exit()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
OWNER = os.getenv("OWNER", "Unknown")

if not API_ID or not API_HASH or not STRING_SESSION:
    print("❌ Missing API credentials in config.env")
    exit()

try:
    from webserver import start_webserver
    start_webserver()
except:
    pass

bot = TelegramClient(StringSession(STRING_SESSION), int(API_ID), API_HASH)
plugins = {}

def load_all_plugins():
    count = 0
    for folder in ["plugins", "plugins/user_plugins"]:
        if not os.path.exists(folder):
            continue
        for file in os.listdir(folder):
            if file.endswith(".py") and file != "__init__.py":
                name = file[:-3]
                module_path = f"{folder.replace('/', '.')}.{name}"
                module = importlib.import_module(module_path)
                plugins[name] = module
                if hasattr(module, "register"):
                    module.register(bot)
                count += 1
    return count

async def start_bot():
    print("══════════════════════════════════════")
    print("🚀 X-OPTIMUS USERBOT STARTING…")
    print("══════════════════════════════════════")

    count = load_all_plugins()

    print("🆔 API ID:", API_ID)
    print("👑 Owner:", OWNER)
    print("📦 Plugins:", count)
    print("🖥 Platform:", platform.system())
    print("🔧 Telethon:", "1.x")
    print("══════════════════════════════════════")

    await bot.start()

    for module in plugins.values():
        if hasattr(module, "on_startup"):
            try:
                await module.on_startup(bot)
            except:
                pass

    print("🟢 BOT ONLINE & RUNNING SUCCESSFULLY")
    print("══════════════════════════════════════")

bot.loop.run_until_complete(start_bot())
bot.run_until_disconnected()
