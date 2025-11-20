from telethon import events
import requests
import os

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/install(?:\s+(.+))?$"))
    async def install_plugin(event):
        url = event.pattern_match.group(1)

        # If no URL given
        if not url:
            await event.reply(
                "❗Usage:\n"
                "`/install {raw_github_url}`\n\n"
                "Example:\n"
                "`/install https://gist.githubusercontent.com/abcd/raw/plugin.py`"
            )
            return

        try:
            url = url.strip()

            # Auto-detect plugin name
            name = url.split("/")[-1].replace(".py", "")
            if not name:
                await event.reply("❌ Invalid plugin name.")
                return

            folder = "plugins/user_plugins"
            os.makedirs(folder, exist_ok=True)

            path = f"{folder}/{name}.py"

            await event.reply("⬇️ Downloading plugin...")

            code = requests.get(url, timeout=20).text

            with open(path, "w", encoding="utf-8") as f:
                f.write(code)

            await event.reply(
                f"✅ Plugin **{name}** installed!\n"
                f"🔄 Reboot bot to activate."
            )

        except Exception as e:
            await event.reply(f"❌ Install Failed:\n`{e}`")
