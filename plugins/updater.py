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

SAFE_FILES = [
    "container_data/config.env",   # <-- ONLY THIS IS PROTECTED
]

def read_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return "0.0.0"
    try:
        with open(LOCAL_VERSION_FILE, "r") as f:
            return json.load(f).get("version", "0.0.0")
    except:
        return "0.0.0"

def read_remote_version():
    try:
        r = requests.get(VERSION_URL).json()
        return r.get("version", "0.0.0"), r.get("changelog", [])
    except:
        return None, None

def register(bot):

    @bot.on(events.NewMessage(pattern="/checkupdate"))  
    async def check(event):  
        local = read_local_version()  
        remote, changes = read_remote_version()  

        if not remote:  
            await event.reply("❌ Could not check update!\nVersion file missing.")  
            return  

        if local == remote:  
            await event.reply(f"✔️ Bot is up-to-date!\nVersion: {local}")  
        else:  
            text = f"⚠️ Update Available!\n\nCurrent: {local}\nLatest: {remote}\n\n📝 Changes:\n"  
            text += "\n".join([f"• {c}" for c in changes])  
            text += "\n\nUse /update to install."  
            await event.reply(text)  

    @bot.on(events.NewMessage(pattern="/update"))  
    async def update(event):  
        msg = await event.reply("⬇️ Downloading update...")  

        try:  
            r = requests.get(ZIP_URL)
            with open("update.zip", "wb") as f:  
                f.write(r.content)  

            await msg.edit("📦 Extracting update...")  

            with zipfile.ZipFile("update.zip", "r") as z:  
                z.extractall("update_temp")  

            folder = os.listdir("update_temp")[0]  
            src = os.path.join("update_temp", folder)  

            for item in os.listdir():  
                if item in SAFE_FILES:
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

            await msg.edit("✅ Update Installed!\n♻️ Restarting bot...")  

            os.execv(sys.executable, ["python3"] + sys.argv)  

        except Exception as e:  
            await msg.edit(f"❌ Update failed!\n`{e}`")
