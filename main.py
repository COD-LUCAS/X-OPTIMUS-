import os
import importlib
import platform
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

CONTAINER_DATA_CFG = "/home/container/container_data/config.env"
CONTAINER_CFG = "/home/container/config.env"
ROOT_CFG = "config.env"

if os.path.isfile(CONTAINER_DATA_CFG):
    load_dotenv(CONTAINER_DATA_CFG)
elif os.path.isfile(CONTAINER_CFG):
    load_dotenv(CONTAINER_CFG)
elif os.path.isfile(ROOT_CFG):
    load_dotenv(ROOT_CFG)
else:
    load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
STRING_SESSION = os.getenv("STRING_SESSION", "")
OWNER = os.getenv("OWNER", "Unknown")

if API_ID == 0 or API_HASH == "" or STRING_SESSION == "":
    print("Missing API credentials")
    exit(1)

IS_RENDER = os.environ.get("RENDER", "false").lower() == "true"

if IS_RENDER:
    try:
        from webserver import start_webserver
        start_webserver()
    except:
        pass

bot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
plugins = {}
BORDER = "═" * 50

def log(t, v):
    print(f"{t:<15}: {v}")

def load_plugins():
    c = 0
    for f in os.listdir("plugins"):
        if f.endswith(".py") and f != "__init__.py":
            n = f[:-3]
            m = importlib.import_module(f"plugins.{n}")
            plugins[n] = m
            if hasattr(m, "register"):
                m.register(bot)
            c += 1
    return c

async def run_startup_events():
    for m in plugins.values():
        if hasattr(m, "on_startup"):
            try:
                await m.on_startup(bot)
            except:
                pass

async def start_bot():
    print(BORDER)
    print("X-OPTIMUS USERBOT STARTING")
    print(BORDER)

    pc = load_plugins()

    log("API ID", API_ID)
    log("Owner", OWNER)
    log("Plugins", pc)
    log("Platform", platform.system())
    log("Telethon", "1.x")

    print(BORDER)

    await bot.start()
    await run_startup_events()

    print("BOT ONLINE & RUNNING SUCCESSFULLY")
    print(BORDER)

bot.loop.run_until_complete(start_bot())
bot.run_until_disconnected()
