from telethon import events
import requests
import json
import os
import asyncio

REMOTE_VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"
LOCAL_VERSION_FILE = "version.json"
LAST_CHECK_FILE = "last_checked_version.txt"


def read_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return "0.0.0"
    try:
        with open(LOCAL_VERSION_FILE, "r") as f:
            return json.load(f).get("version", "0.0.0")
    except:
        return "0.0.0"


def read_remote_version():
    try:
        r = requests.get(REMOTE_VERSION_URL, timeout=10).json()
        return r.get("version", "0.0.0"), r.get("changelog", [])
    except:
        return None, None


async def notify_update_loop(bot):
    while True:
        try:
            local_version = read_local_version()
            remote_version, changelog = read_remote_version()

            if not remote_version:
                await asyncio.sleep(120)
                continue

            # Load previous checked version
            if os.path.exists(LAST_CHECK_FILE):
                with open(LAST_CHECK_FILE, "r") as f:
                    last_notified = f.read().strip()
            else:
                last_notified = "0.0.0"

            # Send message only when remote != local AND remote != last_notified
            if remote_version != local_version and remote_version != last_notified:

                text = (
                    "**⚠️ X-OPTIMUS NEW UPDATE IS THERE!**\n\n"
                    f"**CURRENT VERSION:** `{local_version}`\n"
                    f"**LATEST VERSION:** `{remote_version}`\n\n"
                    "**CHANGE LOG:**\n"
                )

                if changelog:
                    for item in changelog:
                        text += f" - {item}\n"
                else:
                    text += " - No changelog provided\n"

                text += "\nUse **/update** to install the update."

                # SEND TO SAVED MESSAGES
                await bot.send_message("me", text)

                # Save last notified version
                with open(LAST_CHECK_FILE, "w") as f:
                    f.write(remote_version)

        except Exception as e:
            print(f"[update_notify] Error: {e}")

        await asyncio.sleep(120)  # check every 2 minutes


def register(bot):
    bot.loop.create_task(notify_update_loop(bot))
