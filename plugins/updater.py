from telethon import events
import os
import json
import requests
import zipfile
import shutil
import sys

VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"
ZIP_URL = "https://github.com/COD-LUCAS/X-OPTIMUS/archive/refs/heads/main.zip"

LOCAL_VERSION_FILE = "version.json"
SAFE_PATHS = ["container_data/config.env"]

def local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        open(LOCAL_VERSION_FILE, "w").write('{"version":"0.0.0"}')
        return "0.0.0"
    try:
        return json.load(open(LOCAL_VERSION_FILE)).get("version", "0.0.0")
    except:
        return "0.0.0"

def remote_version():
    try:
        r = requests.get(VERSION_URL, verify=False).json()
        return r.get("version", "0.0.0"), r.get("changelog", [])
    except:
        return "0.0.0", []

def safe(p):
    for x in SAFE_PATHS:
        if p == x or p.startswith(x):
            return True
    return False

def find_real_folder(root):
    for dirpath, dirnames, filenames in os.walk(root):
        if "main.py" in filenames:        # core file → correct folder
            return dirpath
    return None

def register(bot):

    @bot.on(events.NewMessage(pattern="/checkupdate"))
    async def check(event):
        lv = local_version()
        rv, changes = remote_version()
        if lv == rv:
            await event.reply(f"✔ Bot is up-to-date\nVersion: {lv}")
        else:
            txt = f"⚠ Update Available\nCurrent: {lv}\nLatest: {rv}\n\n"
            txt += "\n".join([f"- {c}" for c in changes])
            txt += "\n\nUse /update to install."
            await event.reply(txt)

    @bot.on(events.NewMessage(pattern="/update"))
    async def update(event):
        m = await event.reply("Downloading update...")
        try:
            r = requests.get(ZIP_URL, verify=False)
            open("update.zip", "wb").write(r.content)

            await m.edit("Extracting...")

            with zipfile.ZipFile("update.zip", "r") as z:
                z.extractall("update_temp")

            folder = find_real_folder("update_temp")
            if not folder:
                await m.edit("Update failed: main.py not found in ZIP")
                return

            for item in os.listdir():
                if safe(item):
                    continue
                try:
                    if os.path.isfile(item):
                        os.remove(item)
                    else:
                        shutil.rmtree(item)
                except:
                    pass

            for item in os.listdir(folder):
                if safe(item):
                    continue
                s = os.path.join(folder, item)
                d = os.path.join(".", item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

            shutil.rmtree("update_temp")
            os.remove("update.zip")

            await m.edit("Update Installed\nRestarting...")
            os.execv(sys.executable, ["python3"] + sys.argv)

        except Exception as e:
            await m.edit(f"Update failed: {e}")
