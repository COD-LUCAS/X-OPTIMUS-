from telethon import events
import requests
import os
import importlib

USER_PLUGIN_DIR = "plugins/user_plugins"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/install (.+) (.+)$"))
    async def install_plugin(event):
        url = event.pattern_match.group(1).strip()
        name = event.pattern_match.group(2).strip()

        if not name.endswith(".py"):
            name = f"{name}.py"

        if not os.path.exists(USER_PLUGIN_DIR):
            os.makedirs(USER_PLUGIN_DIR)

        save_path = os.path.join(USER_PLUGIN_DIR, name)

        await event.reply("⏳ Downloading plugin...")

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            code = response.text

            with open(save_path, "w", encoding="utf-8") as f:
                f.write(code)

            # AUTO LOAD PLUGIN
            module_path = f"plugins.user_plugins.{name[:-3]}"

            try:
                module = importlib.import_module(module_path)

                if hasattr(module, "register"):
                    module.register(bot)

                await event.reply(f"✅ Plugin `{name}` installed & loaded successfully!")

            except Exception as e:
                await event.reply(f"⚠️ Installed but failed to auto-load:\n`{e}`\nRestart bot!")

        except Exception as e:
            await event.reply(f"❌ Install failed:\n`{e}`")
