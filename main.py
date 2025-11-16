import os
from telethon import TelegramClient, events
from dotenv import load_dotenv
import importlib

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
OWNER = int(os.getenv("OWNER"))
SUDO = list(map(int, os.getenv("SUDO", "").split()))

bot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

def load_plugins():
    for file in os.listdir("plugins"):
        if file.endswith(".py"):
            name = file[:-3]
            module = importlib.import_module("plugins." + name)
            if hasattr(module, "register"):
                module.register(bot)

async def send_startup():
    from plugins.startup import register_startup
    await register_startup(bot, OWNER, SUDO)

@bot.on(events.NewMessage(pattern="/menu"))
async def menu(event):
    installed = []
    for file in os.listdir("plugins"):
        if file.endswith(".py"):
            installed.append(file[:-3])
    text = f"🤖 **X-OPTIMUS MENU**\n\n🔧 Version: 1.0.0\n👑 Owner: COD-LUCAS\n\n📦 **Installed Plugins:**\n"
    for p in installed:
        text += f"• {p}\n"
    await event.reply(text)

async def main():
    load_plugins()
    await bot.start()
    await send_startup()
    print("Bot Started")

bot.loop.run_until_complete(main())
bot.run_until_disconnected()
