from telethon import events
import os
import json
import zipfile
import requests
import shutil

VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"
ZIP_URL = "https://github.com/COD-LUCAS/X-OPTIMUS/archive/refs/heads/main.zip"

SAFE_FILES = [
    "config/config.env",
]

def get_local_version():
    try:
        with open("version.json", "r") as f:
            return json.load(f).get("version", "0.0.0")
    except:
        return "0.0.0"

def get_remote_version():
    try:
        r = requests.get(VERSION_URL).json()
        return r.get("version", "0.0.0"), r.get("changelog", [])
    except:
        return "0.0.0", []

def register(bot):

    @bot.on(events.NewMessage(pattern="/checkupdate"))
    async def check(e):
        msg = await e.reply("🔍 Checking for updates...")
        lv = get_local_version()
        rv, changes = get_remote_version()

        if rv != lv:
            text = f"⚠️ Update Available!\n\nCurrent: `{lv}`\nNew: `{rv}`\n\nChangelog:\n"
            text += "\n".join([f"• {c}" for c in changes])
            text += "\n\nSend `/update` to install."
            await msg.edit(text)
        else:
            await msg.edit(f"✅ Up to date!\nCurrent version: `{lv}`")

    @bot.on(events.NewMessage(pattern="/update"))
    async def updater(e):
        msg = await e.reply("⬇️ Downloading update...")

        try:
            # Download ZIP
            r = requests.get(ZIP_URL)
            with open("update.zip", "wb") as f:
                f.write(r.content)

            await msg.edit("📦 Extracting update...")

            # Extract to temp folder
            with zipfile.ZipFile("update.zip", "r") as zip_ref:
                zip_ref.extractall("update_temp")

            # Detect the extracted folder name dynamically
            folders = os.listdir("update_temp")
            extracted_root = None
            for f in folders:
                if os.path.isdir(f"update_temp/{f}"):
                    extracted_root = f"update_temp/{f}"
                    break

            if not extracted_root:
                return await msg.edit("❌ Update failed!\nCould not detect extracted folder.")

            # Copy everything except SAFE_FILES
            for root, dirs, files in os.walk(extracted_root):
                rel_path = root.replace(extracted_root, "").lstrip("/")
                dst_path = os.path.join(".", rel_path)

                if not os.path.exists(dst_path):
                    os.makedirs(dst_path, exist_ok=True)

                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(dst_path, file)

                    # Do NOT overwrite sensitive files
                    if dst_file.replace("\\", "/") in SAFE_FILES:
                        continue

                    shutil.copy2(src_file, dst_file)

            # Cleanup
            os.remove("update.zip")
            shutil.rmtree("update_temp", ignore_errors=True)

            # Success message
            await msg.edit("✅ Update installed!\n🔄 Restarting...")
            os.execv(sys.executable, ['python'] + sys.argv)

        except Exception as err:
            await msg.edit(f"❌ Update failed!\n`{err}`")
