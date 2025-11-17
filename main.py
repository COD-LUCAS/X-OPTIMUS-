import os
import importlib
import platform
import threading
from telethon import TelegramClient
from telethon.sessions import StringSession
from flask import Flask
from dotenv import load_dotenv

load_dotenv("container_data/config.env")

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

app = Flask(__name__)

@app.route("/")
def home():
    return "X-OPTIMUS USERBOT ONLINE"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def start_web():
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()

bot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
plugins = {}

border = "═" * 50

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

async def start_bot():
    print(border)
    print("🚀 X-OPTIMUS USERBOT STARTING…")
    print(border)

    plugin_count = load_plugins()

    print(f"API ID        : {API_ID}")
    print(f"Platform      : {platform.system()}")
    print(f"Plugins       : {plugin_count}")
    print("Telethon      : 1.x")
    print(border)

    await bot.start()
    print("🟢 USERBOT RUNNING SUCCESSFULLY")
    print(border)

start_web()
bot.loop.run_until_complete(start_bot())
bot.run_until_disconnected()
