from telethon import events
import requests
import os
import zipfile
import shutil

# ==========================
# CONFIG
# ==========================

VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"
ZIP_URL = "https://github.com/COD-LUCAS/X-OPTIMUS/archive/refs/heads/main.zip"

SAFE_KEEP = [
    "config.env",
    "config",
    "config/config.env",
    "startup.jpg",
    "plugins/updater.py",   # protect updater itself
]

# ==========================
# VERSION FUNCTIONS
# ==========================

def get_local_version():
    if os.path.exists("version.json"):
        try:
            return open("version.json").read().strip()
        except:
            return "0.0.0"
    return "0.0.0"

def get_remote_version():
    try:
        r = requests.get(VERSION_URL).json()
        return r.get("version", "0.0.0"), r.get("changelog", [])
    except:
        return "0.0.0", []

# ==========================
# REGISTER EVENTS
# ==========================

def register(bot):

    # -----------------------
    # CHECK UPDATE COMMAND
    # -----------------------
    @bot.on(events.NewMessage(pattern="/checkupdate"))
    async def check(event):
        msg = await event.reply("🔍 **Checking for updates…**")

        local_ver = get_local_version()
        remote_ver, changelog = get_remote_version()

        if remote_ver == local_ver:
            await msg.edit(
                f"🟩 **Up to date!**\n"
                f"Your version: `{local_ver}`\n"
                f"No new updates available 🤝"
            )
        else:
            changes = "\n".join([f"• {c}" for c in changelog])
            await msg.edit(
                f"⚡ **UPDATE AVAILABLE!**\n\n"
                f"🔻 Current Version: `{local_ver}`\n"
                f"🔺 Latest Version: `{remote_ver}`\n\n"
                f"📜 **Changelog:**\n{changes}\n\n"
                f"Run `/update` to install."
            )

    # -----------------------
    # UPDATE COMMAND
    # -----------------------
    @bot.on(events.NewMessage(pattern="/update"))
    async def update(event):
        msg = await event.reply("⬇ **Downloading latest update…**")

        try:
            # Download ZIP
            r = requests.get(ZIP_URL)
            with open("update.zip", "wb") as f:
                f.write(r.content)

            await msg.edit("📦 **Extracting update…**")

            with zipfile.ZipFile("update.zip", "r") as z:
                z.extractall("update_temp")

            folder = os.listdir("update_temp")[0]
            src = os.path.join("update_temp", folder)

            # -------------------
            # CLEAN OLD FILES
            # -------------------
            for item in os.listdir():
                if item in SAFE_KEEP:
                    continue
                try:
                    if os.path.isfile(item):
                        os.remove(item)
                    else:
                        shutil.rmtree(item)
                except:
                    pass

            # -------------------
            # COPY NEW FILES
            # -------------------
            for item in os.listdir(src):
                src_path = os.path.join(src, item)
                if os.path.isfile(src_path):
                    shutil.copy2(src_path, item)
                else:
                    shutil.copytree(src_path, item)

            await msg.edit("✅ **Update installed successfully!**\n♻ Restarting bot…")

            # -------------------
            # AUTO-RESTART
            # -------------------
            os.system("kill 1")

        except Exception as e:
            await msg.edit(f"❌ **Update failed!**\n`{e}`")
