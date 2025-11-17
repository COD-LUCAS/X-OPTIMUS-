import os
import importlib
import platform
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

# ----------------------------------------------------------
# LOAD CONFIG FROM container_data FIRST (safe for Panel/Render)
# ----------------------------------------------------------
CONTAINER_CONFIG = "/home/container_data/config.env"

if os.path.exists(CONTAINER_CONFIG):
    print("[CONFIG] Loading container_data/config.env")
    load_dotenv(CONTAINER_CONFIG)
else:
    print("[CONFIG] Loading local config.env")
    load_dotenv("config/config.env")

# ----------------------------------------------------------
# READ CONFIG VALUES
# ----------------------------------------------------------
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
STRING_SESSION = os.getenv("STRING_SESSION", "")
OWNER = os.getenv("OWNER", "Unknown")

if API_ID == 0 or API_HASH == "" or STRING_SESSION == "":
    print("❌ Missing API credentials in config.env")
    exit(1)

# ----------------------------------------------------------
# START WEB SERVER (Render Needs This)
# ----------------------------------------------------------
try:
    from webserver import start_webserver
    start_webserver()
    print("[WebServer] Started successfully.")
except Exception as e:
    print(f"[WebServer ERROR] {e}")

# ----------------------------------------------------------
# CREATE BOT CLIENT
# ----------------------------------------------------------
bot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
plugins = {}

# ----------------------------------------------------------
# FANCY LOGGING
# ----------------------------------------------------------
BORDER = "═" * 50

def log(title, value):
    print(f"{title:<15}: {value}")

# ----------------------------------------------------------
# LOAD PLUGINS
# ----------------------------------------------------------
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

# ----------------------------------------------------------
# RUN STARTUP EVENTS (startup.py)
# ----------------------------------------------------------
async def run_startup_events():
    for module in plugins.values():
        if hasattr(module, "on_startup"):
            try:
                await module.on_startup(bot)
            except Exception as e:
                print(f"[Startup Error] {e}")

# ----------------------------------------------------------
# MAIN STARTUP FUNCTION
# ----------------------------------------------------------
async def start_bot():
    print(BORDER)
    print("🚀 X-OPTIMUS USERBOT STARTING…")
    print(BORDER)

    plugin_count = load_plugins()

    log("🆔 API ID", API_ID)
    log("👑 Owner", OWNER)
    log("📦 Plugins", plugin_count)
    log("🖥 Platform", platform.system())
    log("🔧 Telethon", "1.x")

    print(BORDER)

    await bot.start()
    await run_startup_events()

    print("🟢 BOT ONLINE & RUNNING SUCCESSFULLY")
    print(BORDER)

# ----------------------------------------------------------
# RUN
# ----------------------------------------------------------
bot.loop.run_until_complete(start_bot())
bot.run_until_disconnected()
