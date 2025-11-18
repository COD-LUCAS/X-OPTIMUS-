import os
import shutil
import zipfile
import requests
from telethon import events

ZIP_URL = "https://github.com/COD-LUCAS/X-OPTIMUS/archive/refs/heads/main.zip"

SAFE = [
    "config_data/config.env",
    "plugins/user_plugins"
]

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/update$"))
    async def update(event):
        msg = await event.reply("⬇️ Downloading update...")

        try:
            if os.path.exists("update_temp"):
                shutil.rmtree("update_temp")
            os.makedirs("update_temp", exist_ok=True)
            
            zdata = requests.get(ZIP_URL, timeout=20, verify=False).content
            open("update.zip", "wb").write(zdata)
        except Exception as e:
            await msg.edit(f"❌ Download failed:\n`{e}`")
            return

        await msg.edit("📦 Extracting update...")

        try:
            with zipfile.ZipFile("update.zip") as z:
                z.extractall("update_temp")
        except Exception as e:
            await msg.edit(f"❌ Extract failed:\n`{e}`")
            return
        finally:
            if os.path.exists("update.zip"):
                os.remove("update.zip")

        try:
            dirlist = [
                d for d in os.listdir("update_temp")
                if os.path.isdir(os.path.join("update_temp", d))
            ]

            if not dirlist:
                await msg.edit("❌ Update failed: No extracted source folder found.")
                return

            extracted = os.path.join("update_temp", dirlist[0])

        except Exception as e:
            await msg.edit(f"❌ Folder detection failed:\n`{e}`")
            return

        await msg.edit("♻️ Replacing files...")

        try:
            for item in os.listdir():
                if item in SAFE or item.startswith("."):
                    continue
                if item == "update_temp":
                    continue 

                if os.path.isfile(item):
                    os.remove(item)
                else:
                    shutil.rmtree(item)

            for item in os.listdir(extracted):
                if item in SAFE:
                    continue

                src = os.path.join(extracted, item)
                dst = item

                if os.path.isdir(src):
                    shutil.copytree(src, dst) 
                else:
                    shutil.copy2(src, dst)

        except Exception as e:
            await msg.edit(f"❌ Update failed during replace:\n`{e}`")
            return
        
        finally:
            if os.path.exists("update_temp"):
                shutil.rmtree("update_temp")

        await msg.edit("✅ Update installed successfully!\nPlease **reboot your bot**.")
        
