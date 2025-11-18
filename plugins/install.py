from telethon import events
import requests, os

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/install (.+) (.+)$"))
    async def install_plugin(event):
        url = event.pattern_match.group(1)
        name = event.pattern_match.group(2)

        folder = "plugins/user_plugins"
        if not os.path.exists(folder):
            os.makedirs(folder)

        path = f"{folder}/{name}.py"

        try:
            code = requests.get(url).text
            with open(path, "w") as f:
                f.write(code)

            await event.reply(f"✅ Plugin `{name}` installed.\nRestart bot to load.")

        except Exception as e:
            await event.reply(f"❌ Install failed:\n`{e}`")
