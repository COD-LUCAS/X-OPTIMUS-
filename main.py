import os
import importlib
import random
import platform
import time
import asyncio
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.functions.channels import JoinChannelRequest

START_TIME = time.time()

def run(cmd):
    try:
        subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        pass

def install_ffmpeg():
    try:
        test = subprocess.run("ffmpeg -version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if test.returncode == 0:
            print("[FFMPEG] Installed ✓")
            return
        print("[FFMPEG] Not found → Installing...")
        run("apt update -y")
        run("apt install ffmpeg -y")
        test2 = subprocess.run("ffmpeg -version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if test2.returncode == 0:
            print("[FFMPEG] Installed Successfully ✓")
        else:
            print("[FFMPEG] Install Failed ✗")
    except:
        print("[FFMPEG] Install Error")

def install_python_packages():
    try:
        import PIL
    except:
        print("[PILLOW] Installing...")
        run("pip install pillow --no-cache-dir")

install_ffmpeg()
install_python_packages()

paths = [
    "container_data/config.env",
    "/home/container/container_data/config.env",
    "/home/container/config.env",
    "config.env"
]

loaded = False
for p in paths:
    if os.path.exists(p):
        load_dotenv(p)
        loaded = True
        break

if not loaded:
    print("config.env not found")
    exit()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
STRING = os.getenv("STRING_SESSION")
OWNER = os.getenv("OWNER", "")

if not API_ID or not API_HASH or not STRING:
    print("Missing API credentials")
    exit()

API_ID = int(API_ID)

bot = TelegramClient(StringSession(STRING), API_ID, API_HASH)
plugins = {}

REACTIONS = ["👍","🔥","😁","❤️","👌","🤝","🎯","✨"]

def color(t,c=37):
    return f"\033[{c}m{t}\033[0m"

def line():
    print(color("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",36))

def load_version():
    try:
        if os.path.exists("version.txt"):
            return open("version.txt").read().strip()
    except:
        pass
    return "v1.0.0"

async def check_session():
    try:
        me = await bot.get_me()
        return f"VALID 🔥 ({me.first_name})"
    except:
        return "INVALID ❌"

async def auto_react(event):
    try:
        emoji = random.choice(REACTIONS)
        await bot(SendReactionRequest(peer=event.chat_id, msg_id=event.id, reaction=[emoji]))
    except:
        pass

_original = bot.add_event_handler

def patched(handler, *a, **kw):
    async def wrap(event):
        if bot.MODE == "PRIVATE" and event.sender_id != bot.owner_id:
            return
        await auto_react(event)
        return await handler(event)
    return _original(wrap, *a, **kw)

bot.add_event_handler = patched

def load_plugins():
    total = 0
    folders = ["plugins", "container_data/user_plugins"]
    for folder in folders:
        if not os.path.isdir(folder):
            continue
        for f in os.listdir(folder):
            if not f.endswith(".py") or f == "__init__.py":
                continue
            name = f[:-3]
            module_path = f"{folder.replace('/', '.')}.{name}"
            try:
                module = importlib.import_module(module_path)
                plugins[name] = module
                if hasattr(module, "register"):
                    module.register(bot)
                total += 1
            except Exception as e:
                print(f"Plugin error ({name}): {e}")
    return total

async def auto_join():
    try:
        await bot(JoinChannelRequest("xoptimusbothelp"))
    except:
        pass

def detect_platform():
    if os.getenv("RENDER"):
        return "RENDER"
    if os.getenv("KOYEB_APP_ID"):
        return "KOYEB"
    if "container" in os.getcwd() or "ptero" in os.getcwd().lower():
        return "PANEL"
    return "LOCAL"

def start_keepalive():
    import requests
    from threading import Thread
    from flask import Flask

    app = Flask(__name__)
    url = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("KOYEB_URL")

    @app.route("/")
    def home():
        return "ok"

    def ping():
        while True:
            if url:
                try:
                    requests.get(url)
                except:
                    pass
            time.sleep(240)

    Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()
    Thread(target=ping).start()

async def show_banner(version, platform_type, plugin_count, session_status):
    os.system("clear || cls")
    line()
    print(color("🚀 X-OPTIMUS STARTING…",35))
    line()
    print(color("▶ SYSTEM INFO",33))
    print(color("Time:",32), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(color("Platform:",32), platform_type)
    print(color("Version:",32), version)
    print(color("KeepAlive:",32),
        "ON (Port Enabled)" if platform_type in ["RENDER","KOYEB"] else "OFF (Panel/Local)")
    print()
    print(color("▶ BOT DETAILS",33))
    print(color("API ID:",32), API_ID)
    print(color("Plugins Loaded:",32), plugin_count)
    print(color("Session:",32), session_status)
    print()
    print(color("🟢 BOT ONLINE",32))
    line()

async def start():
    version = load_version()
    total = load_plugins()
    platform_type = detect_platform()

    if platform_type in ["RENDER", "KOYEB"]:
        start_keepalive()

    await bot.start()

    me = await bot.get_me()
    global OWNER
    if not OWNER:
        OWNER = str(me.id)

    bot.owner_id = int(OWNER)
    bot.MODE = os.getenv("MODE", "PUBLIC").upper()

    await auto_join()

    for p in plugins.values():
        if hasattr(p, "on_startup"):
            try:
                await p.on_startup(bot)
            except:
                pass

    session_status = await check_session()
    await show_banner(version, platform_type, total, session_status)

bot.loop.run_until_complete(start())
bot.run_until_disconnected()
