import os
import requests
from telethon import events

USER_PLUGIN_DIR = "plugins/user_plugins"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/install(?:\s+(https?://\S+)\s+(\S+))?$"))
    async def install_plugin(event):
        url = event.pattern_match.group(1)
        name = event.pattern_match.group(2)

        # If /install used without arguments → show usage
        if not url or not name:
            await event.reply(
                "❗Usage:\n`/install {raw_github_url} {plugin_name}`\n\n"
                "Example:\n`/install https://gist.github.com/raw/123abc/insta.py insta`"
            )
            return

        # Ensure folder exists
        if not os.path.exists(USER_PLUGIN_DIR):
            os.makedirs(USER_PLUGIN_DIR)

        path = os.path.join(USER_PLUGIN_DIR, f"{name}.py")

        try:
            code = requests.get(url).text
            with open(path, "w") as f:
                f.write(code)

            await event.reply(f"✅ Plugin `{name}` installed successfully.\nReboot bot to load it.")

        except Exception as e:
            await event.reply(f"❌ Install failed:\n`{e}`")
