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
        lv = local_ver()
        rv, log = remote_ver()

        if not rv:
            await event.reply("❌ Cannot fetch update info.")
            return

        if lv == rv:
            await event.reply(f"✔ Bot is up-to-date\nVersion: {lv}")
        else:
            msg = "⚠ X-OPTIMUS NEW UPDATE IS THERE\n\n"
            msg += f"CURRENT VERSION: {lv}\n"
            msg += f"LATEST VERSION: {rv}\n\n"
            msg += "CHANGE LOG:\n"
            for i in log:
                msg += f" - {i}\n"
            msg += "\nFOR UPDATE: /update"
            await event.reply(msg)

    @bot.on(events.NewMessage(pattern="/update"))
    async def update(event):
        msg = await event.reply("⬇ Downloading...")

        try:
            data = requests.get(ZIP_URL, verify=False).content
            open("update.zip", "wb").write(data)
        except Exception as e:
            await msg.edit(f"❌ Update failed:\n{e}")
            return

        await msg.edit("📦 Extracting...")

        try:
            with zipfile.ZipFile("update.zip") as z:
                z.extractall("update_temp")
        except Exception as e:
            await msg.edit(f"❌ Extract failed:\n{e}")
            return

        # FIND CORRECT FOLDER DYNAMICALLY
        try:
            dirs = []
            for d in os.listdir("update_temp"):
                p = os.path.join("update_temp", d)
                if os.path.isdir(p):
                    dirs.append(p)

            if not dirs:
                await msg.edit("❌ Update failed: extracted folder missing.")
                return

            src = dirs[0]  # ALWAYS CORRECT
        except Exception as e:
            await msg.edit(f"❌ Update failed during folder detection:\n{e}")
            return

        await msg.edit("🔄 Replacing files...")

        try:
            # DELETE all except SAFE folders
            for x in os.listdir():
                if x in SAFE:
                    continue
                try:
                    if os.path.isfile(x):
                        os.remove(x)
                    else:
                        shutil.rmtree(x)
                except:
                    pass

            # COPY new files
            for x in os.listdir(src):
                s = os.path.join(src, x)
                d = os.path.join(".", x)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

            shutil.rmtree("update_temp")
            os.remove("update.zip")

            await msg.edit("✅ Update Complete!\n♻ Restarting bot...")
            os.execv(sys.executable, ["python3"] + sys.argv)

        except Exception as e:
            await msg.edit(f"❌ Update failed during replace:\n{e}")
