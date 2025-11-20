from telethon import events
import requests
import json
import os

REMOTE_VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"

# Try multiple version.json paths
LOCAL_PATHS = [
    "version.json",
    "./version.json",
    "/home/container/version.json",
    "container/version.json",
    "container_data/version.json",
]


def get_local_version():
    for path in LOCAL_PATHS:
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    return json.load(f).get("version", "0.0.0")
            except:
                return "0.0.0"
    return "0.0.0"


def get_remote_version():
    try:
        r = requests.get(
            REMOTE_VERSION_URL,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        data = r.json()
        return data.get("version"), data.get("changelog", [])
    except:
        return None, None


def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/checkupdate$"))
    async def check_update(event):

        msg = await event.reply("🔍 Checking for updates...")

        local = get_local_version()
        remote, changelog = get_remote_version()

        if not remote:
            return await msg.edit("❌ Could not fetch update info.")

        if local == remote:
            return await msg.edit(
                f"✔️ **Your bot is Up-to-date!**\n\n"
                f"**Current Version:** `{local}`"
            )

        text = (
            "⚠️ **New Update Available!**\n\n"
            f"**Current Version:** `{local}`\n"
            f"**Latest Version:** `{remote}`\n\n"
            "**CHANGE LOG:**\n"
        )

        if changelog:
            for c in changelog:
                text += f" - {c}\n"
        else:
            text += " - No changelog provided\n"

        text += "\nUse **/update** to install the update."

        await msg.edit(text)
