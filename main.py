import os
import importlib
import platform
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

# ------------------------
# LOAD CONFIG
# ------------------------
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
    print("❌ Missing config.env")
    exit()

API_ID = os.getenv("API_ID", "")
API_HASH = os.getenv("API_HASH", "")
STRING = os.getenv("STRING_SESSION", "")
OWNER = os.getenv("OWNER", "")

if not API_ID or not API_HASH or not STRING:
    print("❌ Missing API_ID / API_HASH / STRING_SESSION")
    exit()

API_ID = int(API_ID)

# ------------------------
# START WEBSERVER
# ------------------------
try:
    from webserver import start_webserver
    start_webserver()
except:
    pass

# ------------------------
# START CLIENT
# ------------------------
bot = TelegramClient(StringSession(STRING), API_ID, API_HASH)
plugins = {}

# ------------------------
# LOAD PLUGINS
# ------------------------
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
                    print(f"❌ Plugin error in {name}: {e}")

    return count

# ------------------------
# START BOT
# ------------------------
async def start_bot():
    global OWNER  # allowed

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
    me = await bot.get_me()

    if not OWNER:
        OWNER = str(me.id)

    for m in plugins.values():
        if hasattr(m, "on_startup"):
            try:
                await m.on_startup(bot)
            except Exception as e:
                print("Startup error:", e)

    print("🟢 BOT ONLINE & RUNNING")
    print("══════════════════════")

bot.loop.run_until_complete(start_bot())
bot.run_until_disconnected()
