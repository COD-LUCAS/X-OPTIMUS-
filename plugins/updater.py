from telethon import events
import os, json, requests, zipfile, shutil, sys, ssl

CA = "assets/ca-bundle.crt"

sys.modules['certifi'] = __import__('builtins')
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=CA)

_base = requests.request
def req(method, url, **kw):
    kw["verify"] = CA
    return _base(method, url, **kw)
requests.request = req

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

    @bot.on(events.NewMessage(pattern=r"^/checkupdate$"))
    async def check(event):
        try:
            d = requests.get(VERSION_URL).json()
            remote = d.get("version", "0.0.0")
            log = d.get("changelog", [])
            if os.path.exists("version.json"):
                local = json.load(open("version.json")).get("version", "0.0.0")
            else:
                local = "0.0.0"

            if local == remote:
                return await event.reply(f"✔️ Up-to-date\nVersion: {local}")

            msg = f"⚠️ UPDATE AVAILABLE\n\nCURRENT VERSION: {local}\nLATEST VERSION: {remote}\n\nCHANGE LOG:\n"
            for c in log: msg += f"- {c}\n"
            msg += "\nUse /update to install."
            await event.reply(msg)

        except Exception as e:
            await event.reply(f"❌ Failed:\n`{e}`")


    @bot.on(events.NewMessage(pattern=r"^/update$"))
    async def update(event):
        msg = await event.reply("⬇️ Downloading update...")

        try:
            r = requests.get(ZIP_URL)
            open("update.zip", "wb").write(r.content)

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
                return await msg.edit("❌ Missing update folder.")

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
