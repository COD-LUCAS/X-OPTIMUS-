from telethon import events
import os
import sys
import requests
import zipfile
import shutil
import certifi

VERSION_FILE = "version.txt"
REMOTE_VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.txt"
ZIP_URL = "https://github.com/COD-LUCAS/X-OPTIMUS/archive/refs/heads/main.zip"


# ------------------------------------------
# Get Local Version
# ------------------------------------------
def get_local_version():
    try:
        with open(VERSION_FILE, "r") as f:
            return f.read().strip()
    except:
        return "0"


# ------------------------------------------
# Get Remote Version
# ------------------------------------------
def get_remote_version():
    try:
        r = requests.get(REMOTE_VERSION_URL, verify=certifi.where())
        return r.text.strip()
    except:
        return None


# ------------------------------------------
# Find extracted GitHub folder
# ------------------------------------------
def find_folder():
    for item in os.listdir("update_temp"):
        p = os.path.join("update_temp", item)
        if os.path.isdir(p):
            return p
    return None


# ------------------------------------------
# Register commands
# ------------------------------------------
def register(bot):

    # CHECK UPDATE
    @bot.on(events.NewMessage(pattern="/checkupdate"))
    async def check(event):
        local = get_local_version()
        remote = get_remote_version()

        if remote is None:
            await event.reply("❌ Could not check version (network error).")
            return

        if local == remote:
            await event.reply(f"✔ **Bot is up-to-date!**\nVersion: `{local}`")
        else:
            await event.reply(
                f"🟡 **Update Available!**\n"
                f"Current: `{local}`\n"
                f"Latest: `{remote}`\n"
                f"Run `/update` to install."
            )

    # UPDATE INSTALL
    @bot.on(events.NewMessage(pattern="/update"))
    async def update(event):

        local = get_local_version()
        remote = get_remote_version()

        if remote is None:
            await event.reply("❌ Update error: cannot fetch version.")
            return

        # If same version → skip update
        if local == remote:
            await event.reply(f"✔ **Already up-to-date!**\nVersion: `{local}`")
            return

        msg = await event.reply("⬇ Downloading update...")

        try:
            # DOWNLOAD ZIP
            r = requests.get(ZIP_URL, verify=certifi.where())
            with open("update.zip", "wb") as f:
                f.write(r.content)

            await msg.edit("📦 Extracting update...")

            # EXTRACT
            with zipfile.ZipFile("update.zip", "r") as z:
                z.extractall("update_temp")

            folder = find_folder()
            if not folder:
                await msg.edit("❌ Update failed (folder not found).")
                return

            # REMOVE OLD FILES (safe)
            for item in os.listdir():
                if item in ["config", "update.zip", "update_temp"]:
                    continue
                try:
                    if os.path.isfile(item):
                        os.remove(item)
                    else:
                        shutil.rmtree(item)
                except:
                    pass

            # COPY NEW FILES
            for item in os.listdir(folder):
                s = os.path.join(folder, item)
                d = os.path.join(".", item)

                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

            # SAVE NEW VERSION
            with open("version.txt", "w") as f:
                f.write(remote)

            await msg.edit("✅ **Update Installed!**\n🔄 Restarting bot...")

            os.execv(sys.executable, ['python'] + sys.argv)

        except Exception as e:
            await msg.edit(f"❌ Update failed!\n`{e}`")
