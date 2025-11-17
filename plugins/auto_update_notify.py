from telethon import events
import requests
import json
import asyncio
import os

VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"
CHECK_INTERVAL = 300

LAST_VERSION_FILE = "last_checked_version.txt"

def get_local_version():
    try:
        with open("version.json", "r") as f:
            return json.load(f)["version"]
    except:
        return "0.0.0"

def get_remote_version():
    try:
        r = requests.get(VERSION_URL).json()
        return r["version"], r.get("changelog", [])
    except:
        return "0.0.0", []

async def notify_update(bot):
    await bot.connect()
    owner = int(os.getenv("OWNER_ID"))

    while True:
        lv = get_local_version()
        rv, log = get_remote_version()

        if rv != lv:
            # Prevent repeated notifications
            try:
                with open(LAST_VERSION_FILE, "r") as f:
                    last_notified = f.read().strip()
            except:
                last_notified = None

            if last_notified != rv:
                changelog = "\n".join([f"• {c}" for c in log])

                text = (
                    "⚠️ **New Update Available!**\n\n"
                    f"🔸 **Current:** `{lv}`\n"
                    f"🔹 **New:** `{rv}`\n\n"
                    "📝 **Changelog:**\n"
                    f"{changelog}\n\n"
                    "Send `/update` to install."
                )

                await bot.send_message(owner, text)

                # Save notified version
                with open(LAST_VERSION_FILE, "w") as f:
                    f.write(rv)

        await asyncio.sleep(CHECK_INTERVAL)

def register(bot):
    bot.loop.create_task(notify_update(bot))
