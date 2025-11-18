from telethon import events
import os, json, requests, zipfile, shutil, sys, ssl

cafile = "/etc/ssl/certs/ca-certificates.crt"
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=cafile)

_orig_request = requests.request
def fixed(method, url, **kw):
    kw["verify"] = cafile
    return _orig_request(method, url, **kw)
requests.request = fixed

VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"
ZIP_URL = "https://github.com/COD-LUCAS/X-OPTIMUS/archive/refs/heads/main.zip"

SAFE_ITEMS = [
    "container_data",
    "container_data/config.env",
    "plugins/user_plugins"
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

            extracted = os.listdir("update_temp")
            src = None
            for item in extracted:
                p = os.path.join("update_temp", item)
                if os.path.isdir(p):
                    src = p
                    break

            if not src:
                return await msg.edit("❌ Update folder missing.")

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

            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(".", item)

                if item in SAFE_ITEMS:
                    continue

                if item in ALWAYS_REPLACE and os.path.exists(d):
                    if os.path.isfile(d):
                        os.remove(d)

                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

            shutil.rmtree("update_temp")
            os.remove("update.zip")

            await msg.edit("✅ Update Installed!\n♻ Restarting...")
            os.execv(sys.executable, ["python3"] + sys.argv)

        except Exception as e:
            await msg.edit(f"❌ Update failed:\n`{e}`")
