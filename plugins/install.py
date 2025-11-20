from telethon import events
import requests
import os

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/install(?:\s+(.*))?$"))
    async def install_plugin(event):
        url = event.pattern_match.group(1)

        # If user typed only /install
        if not url:
            return await event.reply("Usage:\n`/install https://raw.githubusercontent.com/.../file.py`")

        # Clean accidental spaces
        url = url.strip()

        # Validate URL
        if not (url.startswith("http://") or url.startswith("https://")):
            return await event.reply("❌ Invalid URL.\nURL must start with http:// or https://")

        # Auto-detect plugin name
        name = url.split("/")[-1].replace(".py", "")
        if not name:
            return await event.reply("❌ Could not detect plugin name.")

        folder = "plugins/user_plugins"
        os.makedirs(folder, exist_ok=True)
        path = f"{folder}/{name}.py"

        try:
            await event.reply("⬇️ Downloading plugin...")

            response = requests.get(url, timeout=20)
            code = response.text

            with open(path, "w", encoding="utf-8") as f:
                f.write(code)

            await event.reply(f"✅ Plugin **{name}** installed successfully!\n🔄 Restart bot to apply changes.")

        except Exception as e:
            await event.reply(f"❌ Install Failed:\n`{e}`")
