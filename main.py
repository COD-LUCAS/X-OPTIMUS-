import os
import importlib
import platform
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

# CONFIG PATHS (Panel + Render)
CONFIGS = [
    "container_data/config.env",
    "/home/container/container_data/config.env",
    "/home/container_data/config.env"
]

# Load config.env
loaded = False
for c in CONFIGS:
    if os.path.exists(c):
        load_dotenv(c)
        loaded = True
        break

if not loaded:
    print("❌ config.env not found in container_data/")
    exit()

# Credentials
API_ID = os.getenv("API_ID", "")
API_HASH = os.getenv("API_HASH", "")
STRING = os.getenv("STRING_SESSION", "")
OWNER = os.getenv("OWNER", "Unknown")

if not API_ID or not API_HASH or not STRING:
    print("❌ Missing API_ID / API_HASH / STRING_SESSION")
    exit()

try:
    API_ID = int(API_ID)
except:
    print("❌ API_ID must be integer")
    exit()

# Try starting webserver
try:
    from webserver import start_webserver
    import threading
    threading.Thread(target=start_webserver, daemon=True).start()
except Exception as e:
    print("⚠️ Webserver disabled:", e)

# Start Telethon
bot = TelegramClient(StringSession(STRING), API_ID, API_HASH)
plugins = {}

# Folders to load plugins from
PLUGIN_FOLDERS = [
    "plugins",
    "container_data/user_plugins"
]

def load_all_plugins():
    total = 0
    for folder in PLUGIN_FOLDERS:
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

                    total += 1
                except Exception as e:
                    print(f"❌ Plugin '{name}' failed: {e}")
    return total

async def start_bot():
    print("══════════════════════")
    print("🚀 X-OPTIMUS STARTING")
    print("══════════════════════")

    total = load_all_plugins()

    print(f"🆔 API ID: {API_ID}")
    print(f"👑 Owner: {OWNER}")
    print(f"📦 Plugins Loaded: {total}")
    print(f"💻 Platform: {platform.system()}")
    print("══════════════════════")

    await bot.start()

    # Startup hooks
    for module in plugins.values():
        if hasattr(module, "on_startup"):
            try:
                await module.on_startup(bot)
            except Exception as e:
                print(f"⚠️ Startup error in plugin: {e}")

    print("🟢 BOT ONLINE & RUNNING")
    print("══════════════════════")

# Start bot
bot.loop.run_until_complete(start_bot())
bot.run_until_disconnected()
