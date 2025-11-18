import os, json, shutil, zipfile, requests
from telethon import events

VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"
ZIP_URL = "https://github.com/COD-LUCAS/X-OPTIMUS/archive/refs/heads/main.zip"

SAFE = [
    "container_data",
    "plugins/user_plugins",
    "version.json",
    "requirements.txt"
]


def local_version():
    try:
        return json.load(open("version.json")).get("version", "0.0.0")
    except:
        return "0.0.0"


def remote_version():
    try:
        r = requests.get(VERSION_URL, timeout=10, verify=False).json()
        return r.get("version"), r.get("changelog", [])
    except:
        return None, []


def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/checkupdate$"))
    async def checkupdate(event):
        lv = local_version()
        rv, log = remote_version()

        if rv is None:
            await event.reply("❌ Could not fetch update info.")
            return

        if lv == rv:
            await event.reply(f"✅ Bot is up-to-date.\nVersion: {lv}")
            return

        text = f"⚠️ **X-OPTIMUS NEW UPDATE AVAILABLE**\n\n"
        text += f"🟣 CURRENT VERSION: `{lv}`\n"
        text += f"🟢 LATEST VERSION: `{rv}`\n\n"
        text += "📄 **CHANGE LOG:**\n"
        for i in log:
            text += f"• {i}\n"
        text += "\n➡️ Use `/update` to install."

        await event.reply(text)

    @bot.on(events.NewMessage(pattern=r"^/update$"))
    async def update(event):
        msg = await event.reply("⬇️ Downloading update...")

        # Download ZIP
        try:
            zdata = requests.get(ZIP_URL, timeout=20, verify=False).content
            open("update.zip", "wb").write(zdata)
        except Exception as e:
            await msg.edit(f"❌ Download failed:\n`{e}`")
            return

        await msg.edit("📦 Extracting update...")

        # Extract ZIP
        try:
            with zipfile.ZipFile("update.zip") as z:
                z.extractall("update_temp")
        except Exception as e:
            await msg.edit(f"❌ Extract failed:\n`{e}`")
            return

        # AUTO-DETECT extracted folder — THIS FIXES YOUR ERROR
        try:
            dirlist = [
                d for d in os.listdir("update_temp")
                if os.path.isdir(os.path.join("update_temp", d))
            ]

            if not dirlist:
                await msg.edit("❌ Update failed: No extracted folder found.")
                return

            extracted = os.path.join("update_temp", dirlist[0])

        except Exception as e:
            await msg.edit(f"❌ Folder detection failed:\n`{e}`")
            return

        await msg.edit("♻️ Replacing files...")

        # Replace files safely
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

        await msg.edit("✅ Update installed successfully!\nPlease restart your bot.")
