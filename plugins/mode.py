import os
from telethon import events
import json

MODE_FILE = "data/mode.txt"
VERSION_FILE = "version.json"

def get_mode():
    try:
        with open(MODE_FILE, "r") as f:
            return f.read().strip()
    except:
        return "public"

def set_mode(m):
    with open(MODE_FILE, "w") as f:
        f.write(m)

def get_version():
    try:
        with open(VERSION_FILE, "r") as f:
            return json.load(f).get("version", "Unknown")
    except:
        return "Unknown"

def register(bot):

    @bot.on(events.NewMessage(pattern="/mode ?(.*)"))
    async def mode_handler(event):
        arg = event.pattern_match.group(1).strip().lower()

        if not arg:
            mode = get_mode()
            return await event.reply(f"🔧 Current mode: **{mode.upper()}**")

        if arg not in ["public", "private"]:
            return await event.reply("❌ Use: `/mode public` or `/mode private`")

        set_mode(arg)
        await event.reply(f"✅ Mode set to **{arg.upper()}**")

    @bot.on(events.NewMessage(pattern="/version"))
    async def version_handler(event):
        v = get_version()
        await event.reply(f"🧩 Current Version: **{v}**")
