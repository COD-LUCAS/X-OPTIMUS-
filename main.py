import os
import importlib
import platform
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

# CONFIG FILES
CONTAINER_CONFIG = "/home/container_data/config.env"
LOCAL_CONFIG = "config/config.env"

if os.path.exists(CONTAINER_CONFIG):
    load_dotenv(CONTAINER_CONFIG)
else:
    load_dotenv(LOCAL_CONFIG)

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
STRING_SESSION = os.getenv("STRING_SESSION", "")
OWNER = os.getenv("OWNER", "Unknown")

if not API_ID or not API_HASH or not STRING_SESSION:
    print("❌ Missing API credentials in config.env")
    exit(1)

# WEB SERVER (Render Support)
try:
    from webserver import start_webserver
    start_webserver()
except:
    pass

# BOT CLIENT
bot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
plugins = {}

# BORDER STYLE
BORDER = "═" * 50


# ------------------------------
# LOAD PLUGINS
# ------------------------------
def load_plugins():
    count = 0

    # OFFICIAL PLUGINS
    for file in os.listdir("plugins"):
        if (
            file.endswith(".py") 
            and file != "__init__.py" 
            and file != "user_plugins"
        ):
            name = file[:-3]
            module = importlib.import_module(f"plugins.{name}")
            plugins[name] = module
            if hasattr(module, "register"):
                module.register(bot)
            count += 1

    # USER INSTALLED PLUGINS
    user_plugin_path = "plugins/user_plugins"
    if not os.path.exists(user_plugin_path):
        os.makedirs(user_plugin_path)

    for file in os.listdir(user_plugin_path):
        if file.endswith(".py"):
            name = file[:-3]
            module = importlib.import_module(f"plugins.user_plugins.{name}")
            plugins[name] = module
            if hasattr(module, "register"):
                module.register(bot)
            count += 1

    return count


# ------------------------------
# STARTUP EVENT HANDLER
# ------------------------------
async def run_startup_events():
    for module in plugins.values():
        if hasattr(module, "on_startup"):
            try:
                await module.on_startup(bot)
            except Exception as e:
                print(f"[Startup Error] {e}")


# ------------------------------
# MAIN START FUNCTION
# ------------------------------
async def start_bot():
    print(BORDER)
    print("🚀 X-OPTIMUS USERBOT STARTING…")
    print(BORDER)

    plugin_count = load_plugins()

    print(f"🆔 API ID       : {API_ID}")
    print(f"👑 OWNER        : {OWNER}")
    print(f"📦 PLUGINS      : {plugin_count}")
    print(f"🖥 PLATFORM     : {platform.system()}")
    print(f"🔧 TELETHON     : 1.x")
    print(BORDER)

    await bot.start()
    await run_startup_events()

    print("🟢 BOT ONLINE & RUNNING SUCCESSFULLY")
    print(BORDER)


# RUN
bot.loop.run_until_complete(start_bot())
bot.run_until_disconnected()
