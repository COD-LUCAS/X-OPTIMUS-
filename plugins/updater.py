from telethon import events
import os, json, requests, zipfile, shutil, sys

VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"
ZIP_URL = "https://github.com/COD-LUCAS/X-OPTIMUS/archive/refs/heads/main.zip"

LOCAL_VERSION_FILE = "version.json"

SAFE_ITEMS = [
    "container_data",                # protect config.env
    "plugins/user_plugins",          # protect user plugins
]

ALWAYS_REPLACE = [
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

            await msg.edit("📦 Extracting update...")

            with zipfile.ZipFile("update.zip", "r") as z:
                z.extractall("update_temp")

            # Detect GitHub folder dynamically
            extracted_items = os.listdir("update_temp")
            if not extracted_items:
                return await msg.edit("❌ Extracted folder empty.")

            src = None
            for item in extracted_items:
                path = os.path.join("update_temp", item)
                if os.path.isdir(path):
                    src = path
                    break

            if not src:
                return await msg.edit("❌ Could not detect update folder.")

            # DELETE all except SAFE folders
            for item in os.listdir():
                if item in SAFE_ITEMS:
                    continue
                if item in ALWAYS_REPLACE:
                    continue
                try:
                    if os.path.isfile(item):
                        os.remove(item)
                    else:
                        shutil.rmtree(item)
                except:
                    pass

            # COPY EVERYTHING FROM UPDATE
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(".", item)

                # Always replace version.json & requirements.txt
                if item in ALWAYS_REPLACE:
                    if os.path.isfile(d):
                        os.remove(d)

                # Skip protected directories
                if item in SAFE_ITEMS:
                    continue

                # Copy updated files
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

            # Cleanup
            shutil.rmtree("update_temp")
            os.remove("update.zip")

            await msg.edit("✅ Update Installed!\n♻ Restarting...")
            os.execv(sys.executable, ["python3"] + sys.argv)

        except Exception as e:
            await msg.edit(f"❌ Update failed:\n`{e}`")
