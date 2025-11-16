import os
import importlib
import platform
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

CONFIG_PATH = "config/config.env"

if not os.path.exists(CONFIG_PATH):
    print("❌ ERROR: config/config.env not found!")
    exit()

load_dotenv(CONFIG_PATH)

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

if not API_ID or not API_HASH or not STRING_SESSION:
    print("❌ Missing values in config/config.env")
    exit()

API_ID = int(API_ID)

bot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
plugins = {}

BORDER = "═" * 50

def pretty_log(a, b):
    print(f"{a:<15}: {b}")

def load_plugins():
    count = 0
    for f in os.listdir("plugins"):
        if f.endswith(".py") and f != "__init__.py":
            name = f[:-3]
            module = importlib.import_module(f"plugins.{name}")
            plugins[name] = module
            if hasattr(module, "register"):
                module.register(bot)
            count += 1
    return count

async def run_startup_events():
    for m in plugins.values():
        if hasattr(m, "on_startup"):
            try:
                await m.on_startup(bot)
            except:
                pass

async def start_bot():
    print(BORDER)
    print("🚀 X-OPTIMUS USERBOT STARTING...")
    print(BORDER)

    plugin_count = load_plugins()

    pretty_log("API ID", API_ID)
    pretty_log("Platform", platform.system())
    pretty_log("Plugins", plugin_count)
    pretty_log("Telethon", "1.x")

    print(BORDER)

    await bot.start()
    await run_startup_events()

    print("🟢 BOT ONLINE & READY")
    print(BORDER)

bot.loop.run_until_complete(start_bot())
bot.run_until_disconnected()
