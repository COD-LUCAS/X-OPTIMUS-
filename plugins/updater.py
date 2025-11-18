from telethon import events
import os
import json
import requests
import zipfile
import shutil
import sys

VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"
ZIP_URL = "https://github.com/COD-LUCAS/X-OPTIMUS/archive/refs/heads/main.zip"

SAFE = [
    "container_data",
    "plugins/user_plugins",
    "version.json"
]

def local_ver():
    try:
        return json.load(open("version.json")).get("version", "0.0.0")
    except:
        return "0.0.0"

def remote_ver():
    try:
        r = requests.get(VERSION_URL, verify=False).json()
        return r.get("version"), r.get("changelog", [])
    except:
        return None, None

def register(bot):

    @bot.on(events.NewMessage(pattern="/checkupdate"))
    async def check(event):
        lv = local_ver()
        rv, log = remote_ver()
        if not rv:
            await event.reply("❌ Cannot fetch update info.")
            return
        if lv == rv:
            await event.reply(f"✔️ Bot is up-to-date\nVersion: {lv}")
        else:
            t = f"⚠️ X-OPTIMUS NEW UPDATE IS THERE\n\n"
            t += f"CURRENT VERSION: {lv}\n"
            t += f"LATEST VERSION: {rv}\n\n"
            t += "CHANGE LOG:\n"
            for i in log:
                t += f" - {i}\n"
            t += "\nFOR UPDATE: /update"
            await event.reply(t)

    @bot.on(events.NewMessage(pattern="/update"))
    async def update(event):
        msg = await event.reply("⬇️ Downloading update...")
        try:
            data = requests.get(ZIP_URL, verify=False).content
            open("update.zip", "wb").write(data)

            await msg.edit("📦 Extracting...")

            with zipfile.ZipFile("update.zip") as z:
                z.extractall("update_temp")

            dirs = os.listdir("update_temp")
            if not dirs:
                await msg.edit("❌ Update failed: no extracted folder.")
                return

            src = os.path.join("update_temp", dirs[0])

            for item in os.listdir():
                if item in SAFE:
                    continue
                try:
                    if os.path.isfile(item):
                        os.remove(item)
                    else:
                        shutil.rmtree(item)
                except:
                    pass

            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(".", item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

            shutil.rmtree("update_temp")
            os.remove("update.zip")

            await msg.edit("✅ Update Installed\n♻️ Restarting...")
            os.execv(sys.executable, ["python3"] + sys.argv)

        except Exception as e:
            await msg.edit(f"❌ Update failed:\n{e}")
