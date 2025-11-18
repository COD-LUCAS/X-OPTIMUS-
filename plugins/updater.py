from telethon import events
import os, json, requests, zipfile, shutil, sys

VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"
ZIP_URL = "https://github.com/COD-LUCAS/X-OPTIMUS/archive/refs/heads/main.zip"

SAFE = [
    "container_data",
    "plugins/user_plugins"
]

def local_ver():
    try:
        return json.load(open("version.json")).get("version","0.0.0")
    except:
        return "0.0.0"

def remote_ver():
    try:
        r = requests.get(VERSION_URL,verify=False).json()
        return r.get("version"),r.get("changelog",[])
    except:
        return None,None

def register(bot):

    @bot.on(events.NewMessage(pattern="/checkupdate"))
    async def check(event):
        lv=local_ver()
        rv,log=remote_ver()
        if not rv:
            await event.reply("❌ Cannot fetch update info.")
            return
        if lv==rv:
            await event.reply(f"✔ Bot is up-to-date\nVersion: {lv}")
        else:
            t="⚠ X-OPTIMUS NEW UPDATE IS THERE\n\n"
            t+=f"CURRENT VERSION: {lv}\n"
            t+=f"LATEST VERSION: {rv}\n\nCHANGE LOG:\n"
            for i in log:
                t+=f" - {i}\n"
            t+="\nFOR UPDATE: /update"
            await event.reply(t)

    @bot.on(events.NewMessage(pattern="/update"))
    async def update(event):
        msg=await event.reply("⬇ Downloading...")
        try:
            z=requests.get(ZIP_URL,verify=False).content
            open("update.zip","wb").write(z)
        except Exception as e:
            await msg.edit(f"❌ Update failed:\n{e}")
            return

        try:
            with zipfile.ZipFile("update.zip") as z:
                z.extractall("update_temp")
        except Exception as e:
            await msg.edit(f"❌ Extract failed:\n{e}")
            return

        # Find the extracted directory
        src = None
        for root, dirs, files in os.walk("update_temp"):
            # Look for a directory that contains expected bot files
            if any(f in files for f in ["main.py", "bot.py", "version.json"]) or \
               any(d in dirs for d in ["plugins", "modules"]):
                src = root
                break
        
        # If not found by content, just use first subdirectory
        if not src:
            items = os.listdir("update_temp")
            for item in items:
                path = os.path.join("update_temp", item)
                if os.path.isdir(path):
                    src = path
                    break

        if not src or not os.path.exists(src):
            await msg.edit("❌ Update failed: cannot find extracted files.")
            if os.path.exists("update_temp"):
                shutil.rmtree("update_temp")
            if os.path.exists("update.zip"):
                os.remove("update.zip")
            return

        try:
            # Remove old files/folders (except safe ones)
            for x in os.listdir():
                if x in SAFE or x in ["update_temp", "update.zip"]:
                    continue
                try:
                    if os.path.isfile(x):
                        os.remove(x)
                    else:
                        shutil.rmtree(x)
                except:
                    pass

            # Copy new files
            for x in os.listdir(src):
                if x in SAFE:
                    continue
                s = os.path.join(src, x)
                d = os.path.join(".", x)
                try:
                    if os.path.isdir(s):
                        if os.path.exists(d):
                            shutil.rmtree(d)
                        shutil.copytree(s, d)
                    else:
                        shutil.copy2(s, d)
                except Exception as e:
                    print(f"Error copying {x}: {e}")

            # Cleanup
            shutil.rmtree("update_temp")
            os.remove("update.zip")

            await msg.edit("✅ Update Complete\n♻ Restarting...")
            os.execv(sys.executable, ["python3"] + sys.argv)

        except Exception as e:
            await msg.edit(f"❌ Update failed during replace:\n{e}")
            # Cleanup on error
            if os.path.exists("update_temp"):
                shutil.rmtree("update_temp")
            if os.path.exists("update.zip"):
                os.remove("update.zip")
