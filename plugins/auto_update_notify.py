import asyncio
import requests
import json
import os

VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"
LAST_FILE = "last_checked_version.txt"


async def notify_update(bot):
    while True:
        try:
            r = requests.get(VERSION_URL).json()
            remote_version = r.get("version", "0.0.0")
            changes = r.get("changelog", [])

            # Load last version
            if os.path.exists(LAST_FILE):
                with open(LAST_FILE, "r") as f:
                    last_version = f.read().strip()
            else:
                last_version = "0.0.0"

            # If new update
            if remote_version != last_version:
                text = (
                    "⚠️ **New Update Available!**\n\n"
                    f"🔹 **Current:** {last_version}\n"
                    f"🔹 **Latest:** {remote_version}\n\n"
                    "📌 **Changelog:**\n"
                )

                if changes:
                    for c in changes:
                        text += f"• {c}\n"
                else:
                    text += "• (No changelog provided)\n"

                text += "\nSend **/update** to install."

                # SEND TO SAVED MESSAGES
                await bot.send_message("me", text)

                # Save new version
                with open(LAST_FILE, "w") as f:
                    f.write(remote_version)

        except Exception as e:
            print(f"[auto_update_notify] Error: {e}")

        await asyncio.sleep(120)  # Check every 2 minutes


def register(bot):
    bot.loop.create_task(notify_update(bot))
