import os
os.environ["RENDER"] = "true"  # Prevent hosting from expecting a web port

import importlib
import platform
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

# Load from config.env (Do NOT allow auto-overwrite)
load_dotenv("config.env")

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

# Create Userbot Client
bot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
plugins = {}

BORDER = "═" * 55

def pretty_log(title, value):
    print(f"{title:<18}: {value}")

def load_plugins():
    count = 0
    for file in os.listdir("plugins"):
        if file.endswith(".py") and file != "__init__.py":
            name = file[:-3]
            try:
                module = importlib.import_module(f"plugins.{name}")
                plugins[name] = module
                if hasattr(module, "register"):
                    module.register(bot)
                count += 1
                print(f"✓ Loaded plugin: {name}")
            except Exception as e:
                print(f"✗ Failed to load {name}: {str(e)}")
    return count

async def run_startup_events():
    for module in plugins.values():
        if hasattr(module, "on_startup"):
            try:
                await module.on_startup(bot)
            except:
                pass

async def start_bot():
    print(BORDER)
    print("🚀  X-OPTIMUS USERBOT STARTING...")
    print(BORDER)

    plugin_count = load_plugins()

    pretty_log("🆔 API ID", API_ID)
    pretty_log("💻 Platform", platform.system())
    pretty_log("📦 Plugins Loaded", plugin_count)
    pretty_log("🔧 Telethon", "1.x Stable")

    print(BORDER)

    await bot.start()
    print("🟢 Telegram Session Connected")

    await run_startup_events()

    print("✨ BOT ONLINE & RUNNING")
    print(BORDER)

# Start the bot loop
bot.loop.run_until_complete(start_bot())
bot.run_until_disconnected()
