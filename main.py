import os
import sys
import importlib
import requests
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ------------------------------- ENV -----------------------------------------

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
STRING = os.environ.get("STRING_SESSION")
OWNER = os.environ.get("OWNER", "Unknown")
VERSION = "1.0.0"

bot = TelegramClient(StringSession(STRING), API_ID, API_HASH)
plugins = {}

os.makedirs("plugins", exist_ok=True)


# ----------------------------- LOAD PLUGINS ---------------------------------

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

                print(f"[PLUGIN] Loaded: {name}")

            except Exception as e:
                print(f"[PLUGIN] Failed: {name} -> {e}")


load_plugins()


# -------------------------- RAW GIST FIX ------------------------------------

def convert_to_raw(url: str):
    if "gist.github.com" in url:
        try:
            parts = url.split("/")
            user = parts[-3]
            gist_id = parts[-1]
            return f"https://gist.githubusercontent.com/{user}/{gist_id}/raw"
        except:
            return url
    return url


# --------------------------- INSTALL PLUGIN ----------------------------------

@bot.on(events.NewMessage(pattern=r"\/install (.+)"))
async def install_plugin(event):
    url = event.pattern_match.group(1)
    url = convert_to_raw(url)

    name = url.split("/")[-1].replace(".py", "")
    path = f"plugins/{name}.py"

    try:
        code = requests.get(url).text

        if "def register" not in code:
            return await event.reply("❌ Invalid plugin file (no register function)")

        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        importlib.invalidate_caches()
        module = importlib.import_module(f"plugins.{name}")
        plugins[name] = module

        if hasattr(module, "register"):
            module.register(bot)

        await event.reply(f"✅ Plugin `{name}` installed!")

    except Exception as e:
        await event.reply(f"❌ Error: `{e}`")


# --------------------------- REMOVE PLUGIN -----------------------------------

@bot.on(events.NewMessage(pattern=r"\/remove (.+)"))
async def remove_plugin(event):
    name = event.pattern_match.group(1)
    path = f"plugins/{name}.py"

    if not os.path.exists(path):
        return await event.reply("❌ Plugin not found.")

    os.remove(path)
    await event.reply(f"🗑 Plugin `{name}` removed.\nRestart required.")


# --------------------------- LIST PLUGINS ------------------------------------

@bot.on(events.NewMessage(pattern=r"\/allplug"))
async def list_plugins(event):
    files = [f[:-3] for f in os.listdir("plugins") if f.endswith(".py")]
    if not files:
        return await event.reply("⚠ No plugins installed.")

    text = "🧩 **Installed Plugins:**\n\n"
    text += "\n".join([f"• `{p}`" for p in files])

    await event.reply(text)


# ------------------------------- ALIVE ---------------------------------------

@bot.on(events.NewMessage(pattern=r"\/alive"))
async def alive(event):
    await event.reply(
        f"🤖 **X-OPTIMUS ONLINE**\n"
        f"━━━━━━━━━━━━━━\n"
        f"🆙 Version: `{VERSION}`\n"
        f"👑 Owner: `{OWNER}`\n"
        f"📌 Python: `{sys.version.split()[0]}`\n"
        f"💻 Platform: `{sys.platform}`"
    )


# ------------------------------- MENU ----------------------------------------

@bot.on(events.NewMessage(pattern=r"\/menu"))
async def menu(event):
    files = [f[:-3] for f in os.listdir("plugins") if f.endswith(".py")]

    text = "🗂 **X-OPTIMUS PLUGIN MENU**\n"
    text += "━━━━━━━━━━━━━━\n"
    text += f"🆙 Version: `{VERSION}`\n"
    text += f"👑 Owner: `{OWNER}`\n\n"
    text += "**Installed Plugins:**\n"
    text += "\n".join([f"• `{p}`" for p in files]) or "No plugins installed."

    await event.reply(text)


# ------------------------------- PING ----------------------------------------

@bot.on(events.NewMessage(pattern=r"\/ping"))
async def ping(event):
    start = asyncio.get_event_loop().time()
    msg = await event.reply("Pinging…")
    end = asyncio.get_event_loop().time()

    await msg.edit(f"🏓 Pong: `{int((end - start) * 1000)}ms`")


# ------------------------------- UPDATE --------------------------------------

@bot.on(events.NewMessage(pattern=r"\/update"))
async def update(event):
    await event.reply("🔄 Updating from GitHub…")

    os.system("git pull")
    await asyncio.sleep(1)

    await event.reply("✅ Updated. Restarting…")
    os.execv(sys.executable, [sys.executable] + sys.argv)


# ------------------------------- RUN BOT -------------------------------------

bot.start()
bot.run_until_disconnected()
