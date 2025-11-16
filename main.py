import os
import sys
import requests
import importlib
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
STRING = os.environ.get("STRING_SESSION")

bot = TelegramClient(StringSession(STRING), API_ID, API_HASH)
plugins = {}

def load_plugins():
    for filename in os.listdir("plugins"):
        if filename.endswith(".py") and filename != "__init__.py":
            name = filename[:-3]
            try:
                module = importlib.import_module(f"plugins.{name}")
                importlib.reload(module)
                plugins[name] = module
                if hasattr(module, "register"):
                    module.register(bot)
            except Exception as e:
                print(f"Failed to load {name}: {e}")

async def send_start_message():
    try:
        img = "assets/start.jpg"
        if os.path.exists(img):
            await bot.send_file(
                "me",
                img,
                caption="🟢 **X-OPTIMUS Started Successfully!**\nBot is now online and running. 🚀"
            )
        else:
            await bot.send_message(
                "me",
                "🟢 **X-OPTIMUS Started Successfully!**\nBot is now online and running. 🚀"
            )
    except:
        pass

load_plugins()

@bot.on(events.NewMessage(pattern=r"^/install (.+)"))
async def install_plugin(event):
    url = event.pattern_match.group(1)
    if not url.startswith("http"):
        return await event.reply("❌ Invalid URL.")

    name = url.split("/")[-1].split("?")[0].replace(".py", "")
    path = f"plugins/{name}.py"

    if os.path.exists(path):
        return await event.reply("⚠ Plugin already exists.")

    try:
        code = requests.get(url).text
        if not code or "def register" not in code:
            return await event.reply("❌ Invalid plugin file.")

        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        importlib.invalidate_caches()
        module = importlib.import_module(f"plugins.{name}")
        plugins[name] = module
        if hasattr(module, "register"):
            module.register(bot)

        await event.reply(f"✅ Installed plugin `{name}.py`")

    except Exception as e:
        await event.reply(f"❌ Error: {e}")


@bot.on(events.NewMessage(pattern=r"^/remove (.+)"))
async def remove_plugin(event):
    name = event.pattern_match.group(1)
    path = f"plugins/{name}.py"

    if not os.path.exists(path):
        return await event.reply("❌ Plugin not found.")

    try:
        os.remove(path)
        plugins.pop(name, None)
        await event.reply(f"🗑 Removed plugin `{name}.py`")
    except Exception as e:
        await event.reply(f"❌ Error: {e}")


@bot.on(events.NewMessage(pattern=r"^/allplug$"))
async def allplug(event):
    if not plugins:
        return await event.reply("⚠ No plugins installed.")
    text = "🔌 **Installed Plugins:**\n\n" + "\n".join(f"• `{p}`" for p in plugins)
    await event.reply(text)


@bot.on(events.NewMessage(pattern=r"^/reboot$"))
async def reboot(event):
    await bot.send_message("me", "🔄 **X-OPTIMUS is restarting…**")
    await event.reply("🔁 Restarting Now…")
    os.execv(sys.executable, [sys.executable] + sys.argv)


print("🚀 X-OPTIMUS USERBOT RUNNING…")

bot.start()
bot.loop.run_until_complete(send_start_message())
bot.run_until_disconnected()
