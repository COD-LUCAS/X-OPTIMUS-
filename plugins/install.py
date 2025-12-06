import os
import re
import requests
from telethon import events

SAVE_DIR = "container_data/user_plugins"
os.makedirs(SAVE_DIR, exist_ok=True)

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/install\s+(.+)"))
    async def install_plugin(event):

        uid = event.sender_id
        mode = bot.mode.lower()

        # OWNER + SUDO CHECK (PUBLIC & PRIVATE)
        if uid != bot.owner_id and uid not in bot.sudo_users:
            return await event.reply("❌ Only owner or sudo members can install plugins.")

        url = event.pattern_match.group(1).strip()
        msg = await event.reply("⬇️ Downloading plugin...")

        url = convert_to_raw_url(url)

        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            code = response.text
        except Exception as e:
            return await msg.edit(f"❌ Failed to download plugin:\n`{e}`")

        name = extract_plugin_name(url)
        commands = extract_commands(code)
        file_path = f"{SAVE_DIR}/{name}.py"

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
        except Exception as e:
            return await msg.edit(f"❌ Write error:\n`{e}`")

        response_msg = f"✅ **Plugin installed successfully!**\n\n"
        response_msg += f"📦 **Name:** `{name}`\n"
        response_msg += f"📍 **Path:** `{file_path}`\n"

        if commands:
            response_msg += f"\n🔧 **Commands found:** ({len(commands)})\n"
            for cmd in commands[:10]:
                response_msg += f"  • `{cmd}`\n"
            if len(commands) > 10:
                response_msg += f"  • *...and {len(commands) - 10} more*\n"
        else:
            response_msg += f"\n⚠️ No commands detected in this plugin.\n"

        response_msg += f"\n🔄 Restart bot using `/reboot` to activate."

        await msg.edit(response_msg)


def convert_to_raw_url(url):
    if "raw.githubusercontent.com" in url:
        return url
    if "github.com" in url and "/blob/" in url:
        return url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    if "gist.github.com" in url:
        if "/raw/" not in url:
            gist_match = re.search(r'gist\.github\.com/[^/]+/([a-f0-9]+)', url)
            if gist_match:
                gist_id = gist_match.group(1)
                try:
                    api_url = f"https://api.github.com/gists/{gist_id}"
                    response = requests.get(api_url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        files = data.get("files", {})
                        if files:
                            for filename, file_data in files.items():
                                if filename.endswith(".py"):
                                    return file_data.get("raw_url")
                            return list(files.values())[0].get("raw_url")
                except:
                    pass
                return f"https://gist.githubusercontent.com/raw/{gist_id}"
        return url
    if "gitlab.com" in url and "/-/blob/" in url:
        return url.replace("/-/blob/", "/-/raw/")
    return url


def extract_plugin_name(url):
    name = url.rstrip('/').split('/')[-1]
    if name.endswith('.py'):
        name = name[:-3]
    name = name.split('?')[0]
    if not name or len(name) < 2:
        name = "plugin"
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    return name


def extract_commands(code):
    commands = []
    pattern1 = re.findall(r'pattern=r?["\'][\^]?(/\w+)', code)
    commands.extend(pattern1)
    pattern2 = re.findall(r'pattern=r?["\'][\^]?(.\w+)', code)
    commands.extend([cmd for cmd in pattern2 if cmd not in commands])
    pattern3 = re.findall(r'CMD\s*=\s*["\'](/\w+)', code)
    commands.extend([cmd for cmd in pattern3 if cmd not in commands])
    seen = set()
    unique_commands = []
    for cmd in commands:
        if cmd not in seen:
            seen.add(cmd)
            unique_commands.append(cmd)
    return unique_commands
