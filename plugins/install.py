from telethon import events
import requests
import os
import importlib

PLUGIN_PATH = "plugins/user_plugins"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/install (.+) (.+)$"))
    async def install_handler(event):

        url = event.pattern_match.group(1).strip()
        name = event.pattern_match.group(2).strip()

        # force extension
        if not name.endswith(".py"):
            name += ".py"

        # create plugin folder if missing
        if not os.path.exists(PLUGIN_PATH):
            os.makedirs(PLUGIN_PATH)

        file_path = f"{PLUGIN_PATH}/{name}"

        await event.reply("⏳ Downloading plugin...")

        try:
            # download code
            r = requests.get(url, timeout=10)
            r.raise_for_status()

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(r.text)

            # load plugin instantly
            module_path = f"plugins.user_plugins.{name[:-3]}"

            try:
                module = importlib.import_module(module_path)
                if hasattr(module, "register"):
                    module.register(bot)

                await event.reply(f"✅ Plugin `{name}` installed & loaded!")

            except Exception as e:
                await event.reply(f"⚠ Installed but load error:\n`{e}`\nRestart bot.")

        except Exception as e:
            await event.reply(f"❌ Install failed:\n`{e}`")
