from telethon import events
import requests
import os
import importlib
import logging

USER_PLUGIN_DIR = "plugins/user_plugins"
logger = logging.getLogger(__name__)

def register(bot):
    print("✓ Install plugin registered")  # Confirm registration

    @bot.on(events.NewMessage(pattern=r"^/install\s+(\S+)\s+(\S+)$"))
    async def install_plugin(event):
        logger.info(f"Install command from {event.sender_id}: {event.raw_text}")
        
        url = event.pattern_match.group(1).strip()
        name = event.pattern_match.group(2).strip()

        if not name.endswith(".py"):
            name = f"{name}.py"

        # Create directory if needed
        os.makedirs(USER_PLUGIN_DIR, exist_ok=True)
        
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
                # Reload if already loaded
                if module_path in importlib.sys.modules:
                    module = importlib.reload(importlib.sys.modules[module_path])
                else:
                    module = importlib.import_module(module_path)

                if hasattr(module, "register"):
                    module.register(bot)
                    await event.reply(f"✅ Plugin `{name}` installed & loaded!")
                else:
                    await event.reply(f"⚠️ Plugin `{name}` installed but has no register() function")

            except Exception as e:
                logger.exception("Failed to load plugin")
                await event.reply(f"⚠️ Installed but failed to auto-load:\n`{e}`\nRestart bot!")

        except Exception as e:
            logger.exception("Failed to install plugin")
            await event.reply(f"❌ Install failed:\n`{e}`")
