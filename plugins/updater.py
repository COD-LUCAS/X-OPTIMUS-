import os
import shutil
import zipfile
import requests
from telethon import events

ZIP_URL = "https://github.com/COD-LUCAS/X-OPTIMUS/archive/refs/heads/main.zip"

SAFE_DIRS = [
    "plugins/user_plugins",
]

SAFE_FILES = [
    "container_data/config.env",
]

def is_safe(path):
    for s in SAFE_DIRS:
        if path == s or path.startswith(s + "/"):
            return True
    for f in SAFE_FILES:
        if path == f:
            return True
    return False

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/update$"))
    async def update(event):

        msg = await event.reply("⬇️ Downloading update...")

        # Download ZIP
        try:
            if os.path.exists("update_temp"):
                shutil.rmtree("update_temp")
            os.makedirs("update_temp", exist_ok=True)

            data = requests.get(ZIP_URL, timeout=20, verify=False).content
            open("update.zip", "wb").write(data)

        except Exception as e:
            return await msg.edit(f"❌ Download failed:\n`{e}`")

        await msg.edit("📦 Extracting update...")

        # Extract ZIP
        try:
            with zipfile.ZipFile("update.zip") as z:
                z.extractall("update_temp")

        except Exception as e:
            return await msg.edit(f"❌ Extraction failed:\n`{e}`")

        finally:
            if os.path.exists("update.zip"):
                os.remove("update.zip")

        # Detect extracted folder
        root_dir = os.listdir("update_temp")[0]
        extracted = os.path.join("update_temp", root_dir)

        # If repo contains X-OPTIMUS folder inside it
        if os.path.exists(os.path.join(extracted, "X-OPTIMUS")):
            extracted = os.path.join(extracted, "X-OPTIMUS")

        await msg.edit("♻️ Updating bot...")

        try:
            # Remove old files EXCEPT SAFE
            for item in os.listdir("."):

                if item in ("update_temp", ".git", ".cache"):
                    continue

                path = item

                if is_safe(path):
                    continue

                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)

            # Copy new files EXCEPT SAFE
            for item in os.listdir(extracted):

                src = os.path.join(extracted, item)
                dst = item

                if is_safe(dst):
                    continue

                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)

        except Exception as e:
            return await msg.edit(f"❌ Update failed:\n`{e}`")

        finally:
            shutil.rmtree("update_temp", ignore_errors=True)

        await msg.edit("✅ Update completed!\nRestart with **/reboot**")
