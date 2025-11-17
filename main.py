import os
import importlib
import platform
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
import asyncio

# ------------------------------------------
#  LOAD STABLE CONFIG FROM PERSISTENT FOLDER
# ------------------------------------------
PERSISTENT_CONFIG = "/home/container_data/config.env"

if os.path.exists(PERSISTENT_CONFIG):
    load_dotenv(PERSISTENT_CONFIG)
else:
    # fallback (first run only)
    load_dotenv("config.env")

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
OWNER = os.getenv("OWNER", "Unknown")

# ------------------------------------------
# Telegram Client
# ------------------------------------------
bot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
plugins = {}

BORDER = "═" * 50


def pretty_log(title, value):
    print(f"{title:<18}: {value}")


# ------------------------------------------
# Load Plugins
# ------------------------------------------
def load_plugins():
    count = 0
    for file in os.listdir("plugins"):
        if file.endswith(".py") and file != "__init__.py":
            name = file[:-3]
            module = importlib.import_module(f"plugins.{name}")
            plugins[name] = module
            if hasattr(module, "register"):
                module.register(bot)
            count += 1
    return count


# ------------------------------------------
# Run Startup Events
# ------------------------------------------
async def run_startup_events():
    for module in plugins.values():
        if hasattr(module, "on_startup"):
            try:
                await module.on_startup(bot)
            except Exception:
                pass


# ------------------------------------------
# Start BOT
# ------------------------------------------
async def start_bot():
    print(BORDER)
    print("🚀 X-OPTIMUS USERBOT STARTING…")
    print(BORDER)

    plugin_count = load_plugins()

    pretty_log("🆔 API ID", API_ID)
    pretty_log("👑 Owner", OWNER)
    pretty_log("💻 Platform", platform.system())
    pretty_log("📦 Plugins Loaded", plugin_count)
    pretty_log("⚙ Telethon", "1.x")

    print(BORDER)

    await bot.start()
    await run_startup_events()

    print("🟢 BOT ONLINE & RUNNING SUCCESSFULLY")
    print(BORDER)


# ------------------------------------------
# RUN LOOP
# ------------------------------------------
bot.loop.run_until_complete(start_bot())
bot.run_until_disconnected()
