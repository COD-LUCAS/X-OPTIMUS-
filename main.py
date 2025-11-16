import os
import sys
import importlib
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
STRING = os.environ.get("STRING_SESSION")

bot = TelegramClient(StringSession(STRING), API_ID, API_HASH)
plugins = {}

os.makedirs("plugins", exist_ok=True)

def load_plugins():
    for file in os.listdir("plugins"):
        if file.endswith(".py") and file != "__init__.py":
            name = file[:-3]
            try:
                module = importlib.import_module(f"plugins.{name}")
                importlib.reload(module)
                plugins[name] = module
                if hasattr(module, "register"):
                    module.register(bot)
                print("Loaded:", name)
            except Exception as e:
                print("Failed:", name, e)

load_plugins()

bot.start()
bot.run_until_disconnected()
