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
        r = requests.get(REMOTE_VERSION_URL, timeout=8)
        r.raise_for_status()
        data = r.json()
        return data.get("version", "0.0.0"), data.get("changelog", [])
    except:
        return None, None


async def notify_update_loop(bot):
    while True:
        try:
            local_ver = read_local_version()
            remote_ver, changelog = read_remote_version()

            if not remote_ver:
                await asyncio.sleep(120)
                continue

            if os.path.exists(LAST_CHECK_FILE):
                with open(LAST_CHECK_FILE, "r") as f:
                    last_notified = f.read().strip()
            else:
                last_notified = "0.0.0"

            if remote_ver != local_ver and remote_ver != last_notified:

                text = (
                    "✦ **X-OPTIMUS UPDATE NOTIFIER** ✦\n"
                    "**by @codlucas**\n"
                    "──────────────────────────\n\n"
                    "**⚠️ New Update Available!**\n\n"
                    f"🔻 **Current Version:** `{local_ver}`\n"
                    f"🔺 **Latest Version:** `{remote_ver}`\n\n"
                    "**📌 Changelog:**\n"
                )

                if changelog:
                    for line in changelog:
                        text += f"• {line}\n"
                else:
                    text += "• No changelog provided\n"

                text += "\nUse **/update** to install this update."

                await bot.send_message("me", text)

                with open(LAST_CHECK_FILE, "w") as f:
                    f.write(remote_ver)

        except Exception as e:
            print(f"[update_notifier] Error: {e}")

        await asyncio.sleep(120)


def register(bot):
    bot.loop.create_task(notify_update_loop(bot))
