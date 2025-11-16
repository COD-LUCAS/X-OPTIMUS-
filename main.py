import os
import importlib
import platform
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

# Load config.env ONLY if present (works on all hosts)
if os.path.exists("config.env"):
    load_dotenv("config.env")

# Universal variable reading (ENV first, config.env second)
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

# Safety check
if not API_ID or not API_HASH or not STRING_SESSION:
    print("\n❌ ERROR: Missing API_ID / API_HASH / STRING_SESSION\n")
    print("➡ Make sure they exist in:")
    print("   • Render: Environment tab")
    print("   • OptiKlink: config.env")
    print("   • Railway: Variables")
    print("   • Koyeb: Runtime > Environment")
    exit()

API_ID = int(API_ID)

# Initialize userbot
bot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
plugins = {}

BORDER = "═" * 50

def pretty_log(n, v):
    print(f"{n:<15}: {v}")

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
    print(BORDER)
    print("🚀 X-OPTIMUS USERBOT STARTING…")
    print(BORDER)

    plugin_count = load_plugins()

    pretty_log("🆔 API ID", API_ID)
    pretty_log("🖥 Platform", platform.system())
    pretty_log("📦 Plugins", plugin_count)
    pretty_log("🔧 Telethon", "1.x")

    print(BORDER)

    await bot.start()
    await run_startup_events()

    print("🟢 BOT ONLINE & READY")
    print(BORDER)

bot.loop.run_until_complete(start_bot())
bot.run_until_disconnected()
