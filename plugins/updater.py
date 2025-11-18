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
        open(LOCAL_VERSION_FILE, "w").write('{"version":"0.0.0","changelog":[]}')
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

def register(bot):

    @bot.on(events.NewMessage(pattern="/checkupdate"))
    async def check(event):
        lv = local_version()
        rv, changes = remote_version()
        if lv == rv:
            await event.reply(f"✔ Bot is up-to-date\nVersion: {lv}")
        else:
            msg = f"⚠ Update Available\nCurrent: {lv}\nLatest: {rv}\n\nChanges:\n"
            msg += "\n".join([f"- {c}" for c in changes])
            msg += "\n\nUse /update to install."
            await event.reply(msg)

    @bot.on(events.NewMessage(pattern="/update"))
    async def update(event):
        m = await event.reply("Downloading update...")
        try:
            r = requests.get(ZIP_URL, verify=False)
            open("update.zip", "wb").write(r.content)

            await m.edit("Extracting...")

            with zipfile.ZipFile("update.zip", "r") as z:
                z.extractall("update_temp")

            folders = [f for f in os.listdir("update_temp")
                       if os.path.isdir(os.path.join("update_temp", f))]

            if not folders:
                await m.edit("Update failed: No folder found")
                return

            src = os.path.join("update_temp", folders[0])

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

            for item in os.listdir(src):
                if safe(item):
                    continue
                s = os.path.join(src, item)
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
