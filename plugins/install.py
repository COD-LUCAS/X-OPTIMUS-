from telethon import events
import requests
import os
import importlib

USER_PLUGIN_DIR = "plugins/user_plugins"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/install (.+) (.+)$"))
    async def install_plugin(event):
        url = event.pattern_match.group(1)
        name = event.pattern_match.group(2)

        if not name.endswith(".py"):
            filename = f"{name}.py"
        else:
            filename = name

        if not os.path.exists(USER_PLUGIN_DIR):
            os.makedirs(USER_PLUGIN_DIR)

        save_path = os.path.join(USER_PLUGIN_DIR, filename)

        await event.reply("⏳ Downloading plugin...")

        try:
            # Fetch plugin content
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            code = response.text

            # Save plugin file
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(code)

            # Try to auto-load plugin without restart
            module_path = f"plugins.user_plugins.{filename[:-3]}"
            try:
                module = importlib.import_module(module_path)
                if hasattr(module, "register"):
                    module.register(bot)
                await event.reply(f"✅ Plugin `{filename}` installed & loaded!")
            except Exception as e:
                await event.reply(f"⚠️ Installed but could not auto-load:\n`{e}`\nRestart bot to load manually.")

        except Exception as e:
            await event.reply(f"❌ Install failed:\n`{e}`")
