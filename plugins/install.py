import os
import requests
from telethon import events

SAVE_DIR = "container_data/user_plugins"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR, exist_ok=True)

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/install\s+(.+)"))
    async def install_plugin(event):
        url = event.pattern_match.group(1)

        msg = await event.reply("⬇️ Downloading plugin...")

        try:
            code = requests.get(url, timeout=20).text
        except:
            return await msg.edit("❌ Failed to download plugin.")

        name = url.split("/")[-1].replace(".py", "")

        file_path = f"{SAVE_DIR}/{name}.py"

        try:
            open(file_path, "w", encoding="utf-8").write(code)
        except Exception as e:
            return await msg.edit(f"❌ Write error:\n`{e}`")

        await msg.edit(
            f"✅ Plugin **{name}** installed successfully!\n"
            f"🔄 Restart bot using `/reboot`"
        )
