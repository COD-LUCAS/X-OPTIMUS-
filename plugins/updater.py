from telethon import events
import os
import json
import zipfile
import shutil
import sys

# Fix SSL certificate issues BEFORE importing requests
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"
ZIP_URL = "https://github.com/COD-LUCAS/X-OPTIMUS/archive/refs/heads/main.zip"

LOCAL_VERSION_FILE = "version.json"

# Files and folders to NEVER delete during update
SAFE_FILES = {
    "container_data",  # Protect entire folder
    "config.env",
    "update_temp",     # Don't delete during update
    "update.zip",      # Don't delete during update
}

def read_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return "0.0.0"
    try:
        with open(LOCAL_VERSION_FILE, "r") as f:
            return json.load(f).get("version", "0.0.0")
    except:
        return "0.0.0"

def read_remote_version():
    try:
        r = requests.get(VERSION_URL, verify=False, timeout=10)
        data = r.json()
        return data.get("version", "0.0.0"), data.get("changelog", [])
    except Exception as e:
        print(f"Version check error: {e}")
        return None, None

def register(bot):

    @bot.on(events.NewMessage(pattern="/checkupdate"))  
    async def check(event):  
        local = read_local_version()  
        remote, changes = read_remote_version()  

        if not remote:  
            await event.reply("❌ Could not check update!\nVersion file missing or network error.")  
            return  

        if local == remote:  
            await event.reply(f"✔️ Bot is up-to-date!\nVersion: {local}")  
        else:  
            text = f"⚠️ New Update Available!\n\n💎 Current: {local}\n💎 Latest: {remote}\n\n🚀 Changelog:\n"  
            text += "\n".join([f"• {c}" for c in changes])  
            text += "\n\nSend /update to install."  
            await event.reply(text)  

    @bot.on(events.NewMessage(pattern="/update"))  
    async def update(event):  
        msg = await event.reply("⬇️ Downloading update...")  

        try:  
            # Download update with SSL disabled
            r = requests.get(ZIP_URL, verify=False, timeout=30)
            r.raise_for_status()
            
            with open("update.zip", "wb") as f:  
                f.write(r.content)  

            await msg.edit("📦 Extracting update...")  

            # Extract to temp folder
            with zipfile.ZipFile("update.zip", "r") as z:  
                z.extractall("update_temp")  

            # Find extracted folder name
            temp_contents = os.listdir("update_temp")
            if not temp_contents:
                raise Exception("Update archive is empty!")
                
            folder = temp_contents[0]  
            src = os.path.join("update_temp", folder)
            
            # Verify source exists
            if not os.path.exists(src):
                raise Exception(f"Extracted folder not found: {src}")

            await msg.edit("🔄 Installing update...")

            # Copy new files FIRST (before deleting anything)
            for item in os.listdir(src):  
                s = os.path.join(src, item)  
                d = os.path.join(".", item)  
                
                # Skip protected items
                if item in SAFE_FILES:
                    print(f"Skipping protected: {item}")
                    continue
                
                try:
                    # Remove destination if exists
                    if os.path.exists(d):
                        if os.path.isdir(d):
                            shutil.rmtree(d)
                        else:
                            os.remove(d)
                    
                    # Copy new files
                    if os.path.isdir(s):  
                        shutil.copytree(s, d)  
                    else:  
                        shutil.copy2(s, d)
                    print(f"Updated: {item}")
                except Exception as e:
                    print(f"Could not update {item}: {e}")

            # Clean up temp files
            try:
                shutil.rmtree("update_temp")
                print("Cleaned up update_temp")
            except Exception as e:
                print(f"Could not remove update_temp: {e}")
            
            try:
                os.remove("update.zip")
                print("Cleaned up update.zip")
            except Exception as e:
                print(f"Could not remove update.zip: {e}")

            await msg.edit("✅ Update Installed!\n♻️ Restarting bot...")  

            # Restart bot
            os.execv(sys.executable, ["python3"] + sys.argv)  

        except Exception as e:  
            error_msg = str(e)
            await msg.edit(f"❌ Update failed!\n`{error_msg[:200]}`")
            
            # Clean up on error
            try:
                if os.path.exists("update_temp"):
                    shutil.rmtree("update_temp")
            except:
                pass
            
            try:
                if os.path.exists("update.zip"):
                    os.remove("update.zip")
            except:
                pass
