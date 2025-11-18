from telethon import events
import requests
import json
import os

REMOTE_VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"
LOCAL_VERSION_FILE = "version.json"


def get_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return "0.0.0"
    try:
        with open(LOCAL_VERSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("version", "0.0.0")
    except:
        return "0.0.0"


def get_remote_version():
    try:
        r = requests.get(REMOTE_VERSION_URL, timeout=10)
        data = r.json()
        return data.get("version"), data.get("changelog", [])
    except:
        return None, None


def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/checkupdate$"))
    async def check_update(event):

        await event.reply("🔍 Checking for updates...")

        local = get_local_version()
        remote, changelog = get_remote_version()

        if not remote:
            return await event.reply("❌ Could not fetch update info.")

        if local == remote:
            return await event.reply(f"✔️ Your bot is Up-to-date!\n\n**Current Version:** `{local}`")

        msg = (
            "⚠️ **New Update Available!**\n\n"
            f"**Current Version:** `{local}`\n"
            f"**Latest Version:** `{remote}`\n\n"
            "**CHANGE LOG:**\n"
        )

        if changelog:
            for c in changelog:
                msg += f" - {c}\n"
        else:
            msg += " - No changelog provided\n"

        msg += "\nUse **/update** to install the update."

        await event.reply(msg)
