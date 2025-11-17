import os
import importlib
import platform
import threading
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
from flask import Flask

# Load config.env
load_dotenv("config/config.env")

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

# Flask keep-alive (REQUIRED for Render Web Services)
app = Flask(__name__)

@app.route("/")
def home():
    return "X-OPTIMUS USERBOT RUNNING"

def run_keepalive():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def start_keepalive():
    t = threading.Thread(target=run_keepalive)
    t.start()

# Userbot setup
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

async def run_startup():
    for module in plugins.values():
        if hasattr(module, "on_startup"):
            try:
                await module.on_startup(bot)
            except:
                pass

async def start_bot():
    print(BORDER)
    print("🚀 X-OPTIMUS USERBOT STARTING…")
    print(BORDER)

    plugin_count = load_plugins()

    pretty_log("🆔 API ID", API_ID)
    pretty_log("💻 Platform", platform.system())
    pretty_log("📦 Plugins", plugin_count)
    pretty_log("🔧 Telethon", "1.x")
    print(BORDER)

    await bot.start()
    await run_startup()

    print("🟢 USERBOT RUNNING SUCCESSFULLY")
    print(BORDER)

# Start keepalive server
start_keepalive()

# Start Userbot
bot.loop.run_until_complete(start_bot())
bot.run_until_disconnected()
