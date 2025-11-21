import os
import importlib
import platform
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

CONFIGS = [
    "container_data/config.env",
    "/home/container/container_data/config.env",
    "/home/container/config.env"
]

for c in CONFIGS:
    if os.path.exists(c):
        load_dotenv(c)
        break

API_ID = os.getenv("API_ID", "")
API_HASH = os.getenv("API_HASH", "")
STRING = os.getenv("STRING_SESSION", "")
OWNER = os.getenv("OWNER", "")

if not API_ID or not API_HASH or not STRING:
    print("Missing API_ID / API_HASH / STRING_SESSION")
    exit()

API_ID = int(API_ID)

try:
    from webserver import start_webserver
    start_webserver()
except:
    pass

bot = TelegramClient(StringSession(STRING), API_ID, API_HASH)
plugins = {}

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

async def start_bot():
    global OWNER

    total = load_plugins()
    await bot.start()
    me = await bot.get_me()
    OWNER = str(me.id)

    config_file = "container_data/config.env"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            lines = f.readlines()

        found = False
        for i in range(len(lines)):
            if lines[i].startswith("OWNER="):
                lines[i] = f"OWNER={OWNER}\n"
                found = True

        if not found:
            lines.append(f"OWNER={OWNER}\n")

        with open(config_file, "w") as f:
            f.writelines(lines)

    print("══════════════════════")
    print("🚀 X-OPTIMUS STARTING")
    print("══════════════════════")
    print("🆔 API ID:", API_ID)
    print("👑 Owner:", OWNER)
    print("📦 Plugins Loaded:", total)
    print("💻 Platform:", platform.system())
    print("══════════════════════")

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
