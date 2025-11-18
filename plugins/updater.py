import os, json, shutil, zipfile, requests
from telethon import events

VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"
ZIP_URL = "https://github.com/COD-LUCAS/X-OPTIMUS/archive/refs/heads/main.zip"

SAFE = ["container_data", "plugins/user_plugins", "version.json"]


def get_local_version():
    try:
        return json.load(open("version.json")).get("version", "0.0.0")
    except:
        return "0.0.0"


def get_remote():
    try:
        r = requests.get(VERSION_URL, timeout=10, verify=False).json()
        return r.get("version"), r.get("changelog", [])
    except:
        return None, None


def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/checkupdate$"))
    async def checkupdate(event):
        lv = get_local_version()
        rv, log = get_remote()

        if rv is None:
            await event.reply("❌ Cannot fetch update info.")
            return

        if lv == rv:
            await event.reply(f"✅ Bot is already up-to-date.\nVersion: {lv}")
            return

        txt = f"⚠️ **X-OPTIMUS NEW UPDATE IS THERE**\n\n"
        txt += f"🟣 CURRENT VERSION: `{lv}`\n"
        txt += f"🟢 LATEST VERSION: `{rv}`\n\n"
        txt += "📄 **CHANGE LOG:**\n"
        for i in log:
            txt += f"• {i}\n"
        txt += "\n➡️ Update using: `/update`"

        await event.reply(txt)

    @bot.on(events.NewMessage(pattern=r"^/update$"))
    async def update(event):
        msg = await event.reply("⬇️ Downloading update...")

        try:
            data = requests.get(ZIP_URL, timeout=20, verify=False).content
            open("update.zip", "wb").write(data)
        except Exception as e:
            await msg.edit(f"❌ Update failed:\n`{e}`")
            return

        await msg.edit("📦 Extracting update...")

        try:
            with zipfile.ZipFile("update.zip") as z:
                z.extractall("update_temp")
        except Exception as e:
            await msg.edit(f"❌ Extraction failed:\n`{e}`")
            return

        # FIND REAL FOLDER (GitHub renames it automatically)
        try:
            dirs = [d for d in os.listdir("update_temp") if os.path.isdir(os.path.join("update_temp", d))]
            if not dirs:
                await msg.edit("❌ Update failed: extracted folder missing.")
                return

            src = os.path.join("update_temp", dirs[0])

        except Exception as e:
            await msg.edit(f"❌ Update failed:\n`{e}`")
            return

        await msg.edit("♻️ Replacing files...")

        try:
            for item in os.listdir():
                if item in SAFE:
                    continue
                if item.startswith("."):
                    continue

                if os.path.isfile(item):
                    os.remove(item)
                else:
                    shutil.rmtree(item)

            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(item)
                if item in SAFE:
                    continue
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)

        except Exception as e:
            await msg.edit(f"❌ Update failed during replace:\n`{e}`")
            return

        await msg.edit("✅ Update installed!\nPlease restart your bot.")
