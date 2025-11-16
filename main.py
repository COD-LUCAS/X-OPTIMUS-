import os
import importlib
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

bot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
plugins = {}

def load_plugins():
    for file in os.listdir("plugins"):
        if file.endswith(".py") and file != "__init__.py":
            name = file[:-3]
            module = importlib.import_module(f"plugins.{name}")
            plugins[name] = module
            if hasattr(module, "register"):
                module.register(bot)

async def run_startup_events():
    for module in plugins.values():
        if hasattr(module, "on_startup"):
            try:
                await module.on_startup(bot)
            except:
                pass

async def start_bot():
    load_plugins()
    await bot.start()
    await run_startup_events()
    print("X-OPTIMUS USERBOT RUNNING")

bot.loop.run_until_complete(start_bot())
bot.run_until_disconnected()
