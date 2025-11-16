from telethon import events
import os
import sys
import json
import requests
import zipfile
import shutil

VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"
ZIP_URL = "https://github.com/COD-LUCAS/X-OPTIMUS/archive/refs/heads/main.zip"


def parse(v):
    try:
        return tuple(map(int, v.split(".")))
    except:
        return (0,)


def local_version():
    try:
        with open("version.json", "r") as f:
            return json.load(f).get("version", "0.0.0")
    except:
        return "0.0.0"


def remote_version():
    r = requests.get(VERSION_URL).json()
    return r.get("version", "0.0.0"), r.get("changelog", [])


def register(bot):

    @bot.on(events.NewMessage(pattern="/checkupdate"))
    async def check(event):
        msg = await event.reply("🔍 Checking updates…")
        lv = local_version()
        rv, changes = remote_version()
        if parse(rv) > parse(lv):
            cl = "\n".join(f"• {c}" for c in changes)
            await msg.edit(f"🆕 Update available\nCurrent: `{lv}`\nLatest: `{rv}`\n\n{cl}\n\nUse /update")
        else:
            await msg.edit(f"✅ Up to date\nCurrent version: `{lv}`")

    @bot.on(events.NewMessage(pattern="/update"))
    async def update(event):
        msg = await event.reply("⬇ Downloading latest version…")

        try:
            r = requests.get(ZIP_URL)
            with open("update.zip", "wb") as f:
                f.write(r.content)

            await msg.edit("📦 Extracting update…")

            with zipfile.ZipFile("update.zip", "r") as z:
                z.extractall("update_temp")

            folder = os.listdir("update_temp")[0]
            src = os.path.join("update_temp", folder)

            for item in os.listdir():
                if item not in ["update.zip", "update_temp"]:
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
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)

            shutil.rmtree("update_temp")
            os.remove("update.zip")

            await msg.edit("✅ Update installed\n🔁 Restarting…")
            os.execv(sys.executable, [sys.executable] + sys.argv)

        except Exception as e:
            await msg.edit(f"❌ Update failed\n`{e}`")
