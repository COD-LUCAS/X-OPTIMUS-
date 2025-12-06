from telethon import events
import requests
import json
import os

REMOTE_VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"

LOCAL_PATHS = [
    "version.json",
    "./version.json",
    "/home/container/version.json",
    "/home/container_data/version.json",
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

        uid = event.sender_id

        # FIXED OWNER + SUDO PERMISSION
        if uid != bot.owner_id and uid not in bot.sudo_users:
            return await event.reply("❌ Only owner or sudo can check updates.")

        msg = await event.reply("🔍 Checking for updates...")

        local = get_local_version()
        remote, changelog = get_remote_version()

        if not remote:
            return await msg.edit("❌ Could not fetch update information.")

        if local == remote:
            return await msg.edit(
                f"✔ **Your bot is up-to-date.**\n\n"
                f"📌 Version: `{local}`"
            )

        text = (
            "⚠ **New Update Available!**\n\n"
            f"📌 Current Version: `{local}`\n"
            f"📌 Latest Version: `{remote}`\n\n"
            "**CHANGELOG:**\n"
        )

        if changelog:
            for line in changelog:
                text += f"• {line}\n"
        else:
            text += "• No changelog provided\n"

        text += "\nUse **/update** to install the update."

        await msg.edit(text)
