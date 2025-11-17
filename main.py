import os
import importlib
import platform
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

from keep_alive import keep_alive  # <--- IMPORTANT

load_dotenv("config.env")

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

bot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
plugins = {}

BORDER = "═" * 50

def pretty_log(title, value):
    print(f"{title:<15}: {value}")

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

async def run_startup_events():
    for module in plugins.values():
        if hasattr(module, "on_startup"):
            try:
                await module.on_startup(bot)
            except:
                pass

async def start_bot():

    keep_alive()  # <---- START WEB SERVER BEFORE BOT

    print(BORDER)
    print("🚀 X-OPTIMUS USERBOT STARTING…")
    print(BORDER)

    plugin_count = load_plugins()

    pretty_log("🆔 API ID", API_ID)
    pretty_log("👁 Platform", platform.system())
    pretty_log("📦 Plugins", plugin_count)
    pretty_log("🔧 Telethon", "1.x")

    print(BORDER)

    await bot.start()
    await run_startup_events()

    print("🟢 BOT ONLINE & RUNNING SUCCESSFULLY")
    print(BORDER)

bot.loop.run_until_complete(start_bot())
bot.run_until_disconnected()
