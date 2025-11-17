from telethon import events
import os
import sys
import json
import zipfile
import shutil
import requests
import certifi

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
    r = requests.get(VERSION_URL, verify=certifi.where()).json()
    return r.get("version", "0.0.0"), r.get("changelog", [])

def find_extracted_folder():
    items = os.listdir("update_temp")
    for i in items:
        path = os.path.join("update_temp", i)
        if os.path.isdir(path):
            return path
    return None


def register(bot):

    # ---------- CHECK UPDATE ----------
    @bot.on(events.NewMessage(pattern="/checkupdate"))
    async def check(event):

        msg = await event.reply("🔍 Checking updates…")

        lv = local_version()
        rv, changes = remote_version()

        if parse(rv) > parse(lv):
            cl = "\n• " + "\n• ".join(changes) if changes else ""
            await msg.edit(
                f"🟡 **Update Available!**\n\n"
                f"➡ Current: **{lv}**\n"
                f"➡ Latest: **{rv}**\n"
                f"{cl}\n\nUse **/update** to install."
            )
        else:
            await msg.edit(f"✔ **Bot is already up-to-date!**\nVersion: **{lv}**")

    # ---------- INSTALL UPDATE ----------
    @bot.on(events.NewMessage(pattern="/update"))
    async def update(event):

        msg = await event.reply("⬇ Downloading latest version…")

        try:
            r = requests.get(ZIP_URL, verify=certifi.where())
            with open("update.zip", "wb") as f:
                f.write(r.content)

            await msg.edit("📦 Extracting update…")

            with zipfile.ZipFile("update.zip", "r") as z:
                z.extractall("update_temp")

            folder = find_extracted_folder()
            if not folder:
                await msg.edit("❌ Update failed!\nCould not detect extracted folder.")
                return

            src = folder

            # Delete old files except config
            for item in os.listdir():
                if item in ["config", "update_temp", "update.zip"]:
                    continue
                try:
                    if os.path.isfile(item):
                        os.remove(item)
                    else:
                        shutil.rmtree(item)
                except:
                    pass

            # Copy new files
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(".", item)

                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

            await msg.edit("✅ **Update Installed Successfully!**\n🔄 Restarting…")

            os.execv(sys.executable, ['python'] + sys.argv)

        except Exception as e:
            await msg.edit(f"❌ Update failed!\n`{e}`")
