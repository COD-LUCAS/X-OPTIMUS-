import os
import shutil
import zipfile
import requests
from telethon import events

ZIP_URL = "https://github.com/COD-LUCAS/X-OPTIMUS/archive/refs/heads/main.zip"
ENV_FILE = "config.env"

SAFE_DIRS = ["container_data"]


def is_safe(path):
    for s in SAFE_DIRS:
        if path == s or path.startswith(s + "/"):
            return True
    return False


def get_owner_id():
    if not os.path.exists(ENV_FILE):
        return None

    with open(ENV_FILE, "r") as f:
        for line in f:
            if line.startswith("OWNER_ID="):
                return int(line.replace("OWNER_ID=", "").strip())

    return None


def save_owner_id(uid):
    lines = []
    found = False

    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if line.startswith("OWNER_ID="):
                lines[i] = f"OWNER_ID={uid}\n"
                found = True
                break

    if not found:
        lines.append(f"OWNER_ID={uid}\n")

    with open(ENV_FILE, "w") as f:
        f.writelines(lines)


def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/update$"))
    async def update(event):

        # Load existing owner ID if available
        owner_id = get_owner_id()

        # Auto-detect owner if not saved yet
        if owner_id is None:
            owner_id = (await bot.get_me()).id
            save_owner_id(owner_id)

        # Permission check
        if event.sender_id != owner_id:
            return await event.reply("❌ Only the bot owner can update the bot.")

        msg = await event.reply("⬇️ Downloading update...")

        # Download ZIP
        try:
            if os.path.exists("update_temp"):
                shutil.rmtree("update_temp")
            os.makedirs("update_temp", exist_ok=True)

            data = requests.get(ZIP_URL, timeout=20, verify=False).content
            open("update.zip", "wb").write(data)
        except Exception as e:
            return await msg.edit(f"❌ Download failed:\n`{e}`")

        # Extract
        await msg.edit("📦 Extracting update...")

        try:
            with zipfile.ZipFile("update.zip") as z:
                z.extractall("update_temp")
        except Exception as e:
            return await msg.edit(f"❌ Extraction failed:\n`{e}`")
        finally:
            if os.path.exists("update.zip"):
                os.remove("update.zip")

        extracted_root = os.listdir("update_temp")[0]
        extracted = os.path.join("update_temp", extracted_root)

        if os.path.isdir(os.path.join(extracted, "X-OPTIMUS")):
            extracted = os.path.join(extracted, "X-OPTIMUS")

        # Apply update
        await msg.edit("♻️ Updating files...")

        try:
            # Remove old files
            for item in os.listdir("."):
                if item == "update_temp":
                    continue
                if is_safe(item):
                    continue
                if item.startswith(".git"):
                    continue

                if os.path.isfile(item):
                    os.remove(item)
                else:
                    shutil.rmtree(item)

            # Copy new files
            for item in os.listdir(extracted):
                src = os.path.join(extracted, item)
                dst = item

                if is_safe(dst):
                    continue

                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)

        except Exception as e:
            return await msg.edit(f"❌ Update failed:\n`{e}`")

        shutil.rmtree("update_temp", ignore_errors=True)
        await msg.edit("✅ Update successful! Use /reboot")
