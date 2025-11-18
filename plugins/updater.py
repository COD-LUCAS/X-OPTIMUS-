from telethon import events
import os, json, requests, zipfile, shutil, sys

VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"
ZIP_URL = "https://github.com/COD-LUCAS/X-OPTIMUS/archive/refs/heads/main.zip"

SAFE_KEEP = [
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
            await event.reply("❌ Cannot fetch version.")
            return

        if lv == rv:
            await event.reply(f"✔ Up to date\nVersion {lv}")
        else:
            text = (
                "⚠ X-OPTIMUS NEW UPDATE IS THERE\n\n"
                f"CURRENT VERSION: {lv}\n"
                f"LATEST VERSION: {rv}\n\n"
                "CHANGE LOG:\n" +
                "\n".join(f" - {c}" for c in log) +
                "\n\nFor update: /update"
            )
            await event.reply(text)

    @bot.on(events.NewMessage(pattern="/update"))
    async def updater(event):
        msg = await event.reply("⬇ Downloading update...")

        try:
            content = requests.get(ZIP_URL, verify=False).content
            open("update.zip", "wb").write(content)
        except Exception as e:
            await msg.edit(f"❌ Update failed:\n{e}")
            return

        # Extract
        try:
            with zipfile.ZipFile("update.zip") as z:
                z.extractall("update_temp")
        except Exception as e:
            await msg.edit(f"❌ Extraction failed:\n{e}")
            return

        # Find extracted folder automatically
        try:
            folders = [f for f in os.listdir("update_temp")]
            if not folders:
                await msg.edit("❌ Extracted folder missing.")
                return

            src = os.path.join("update_temp", folders[0])
            if not os.path.isdir(src):
                await msg.edit("❌ Extracted folder invalid.")
                return
        except:
            await msg.edit("❌ Cannot read extracted folder.")
            return

        # Safe replacement (ONLY after full extraction success)
        try:
            for item in os.listdir():
                if item in SAFE_KEEP:
                    continue
                try:
                    path = os.path.join(".", item)
                    if os.path.isfile(path):
                        os.remove(path)
                    else:
                        shutil.rmtree(path)
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

            shutil.rmtree("update_temp")
            os.remove("update.zip")

            await msg.edit("✅ Update complete.\n♻ Restarting...")
            os.execv(sys.executable, ["python3"] + sys.argv)

        except Exception as e:
            await msg.edit(f"❌ Update failed during replace:\n{e}")
