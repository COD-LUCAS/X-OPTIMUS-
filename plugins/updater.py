from telethon import events
import os, json, requests, zipfile, shutil, sys

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
        await event.reply("🔍 Checking for updates...")
        lv = local_ver()
        rv, log = remote_ver()

        if not rv:
            await event.reply("❌ Could not fetch update info.")
            return

        if lv == rv:
            await event.reply(f"✔ Bot is up-to-date.\nVersion: {lv}")
        else:
            txt = (
                f"⚠ X-OPTIMUS NEW UPDATE IS THERE\n\n"
                f"🟣 CURRENT VERSION: {lv}\n"
                f"🟢 LATEST VERSION: {rv}\n\n"
                f"📌 CHANGE LOG:\n"
            )
            for i in log:
                txt += f" - {i}\n"
            txt += "\nFOR UPDATE /update"
            await event.reply(txt)

    @bot.on(events.NewMessage(pattern="/update"))
    async def update(event):
        msg = await event.reply("⬇ Downloading update...")

        try:
            data = requests.get(ZIP_URL, verify=False).content
            open("update.zip", "wb").write(data)

            await msg.edit("📦 Extracting...")

            with zipfile.ZipFile("update.zip", "r") as z:
                z.extractall("update_temp")

            dirs = [
                d for d in os.listdir("update_temp")
                if os.path.isdir(os.path.join("update_temp", d))
            ]

            if not dirs:
                await msg.edit("❌ Update failed: No extracted folder found.")
                return

            src = os.path.join("update_temp", dirs[0])

            await msg.edit("🔄 Replacing files...")

            for x in os.listdir():
                safe_match = any(x == s or x.startswith(s) for s in SAFE)
                if safe_match:
                    continue

                try:
                    if os.path.isfile(x):
                        os.remove(x)
                    else:
                        shutil.rmtree(x)
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

            await msg.edit("✅ Update Installed!\n♻ Restarting bot...")
            os.execv(sys.executable, ["python3"] + sys.argv)

        except Exception as e:
            await msg.edit(f"❌ Update failed during replace:\n`{e}`")
