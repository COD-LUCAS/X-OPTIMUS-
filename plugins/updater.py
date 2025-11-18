from telethon import events
import os, json, requests, zipfile, shutil, sys

VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"
ZIP_URL = "https://github.com/COD-LUCAS/X-OPTIMUS/archive/refs/heads/main.zip"

LOCAL_VERSION_FILE = "version.json"

SAFE_FILES = [
    "container_data",
    "container_data/config.env",
    "plugins/user_plugins",  # ← DO NOT DELETE USER PLUGINS
    "version.json",
    "requirements.txt"
]

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/update$"))
    async def update(event):
        msg = await event.reply("⬇️ Downloading update...")
        try:
            r = requests.get(ZIP_URL)
            open("update.zip", "wb").write(r.content)

            with zipfile.ZipFile("update.zip", "r") as z:
                z.extractall("update_temp")

            folder = os.listdir("update_temp")[0]
            src = os.path.join("update_temp", folder)

            # delete everything except SAFE_FILES
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

            # copy update
            for item in os.listdir(src):
                if item in SAFE_FILES:
                    continue
                s = os.path.join(src, item)
                d = os.path.join(".", item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

            shutil.rmtree("update_temp")
            os.remove("update.zip")

            await msg.edit("✅ Update Installed!\nRestarting...")
            os.execv(sys.executable, ["python3"] + sys.argv)

        except Exception as e:
            await msg.edit(f"❌ Update failed:\n`{e}`")
