import os
from telethon import events

USER_PLUGIN_DIR = "plugins/user_plugins"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/remove(?:\s+(.+))?$"))
    async def remove_plugin(event):
        name = event.pattern_match.group(1)

        # If no plugin name → show usage
        if not name:
            await event.reply("❗Usage:\n`/remove {plugin_name}`\n\nTo remove installed plugins only.")
            return

        name = name.strip()
        plugin_path = os.path.join(USER_PLUGIN_DIR, f"{name}.py")

        if not os.path.exists(plugin_path):
            await event.reply(
                f"❌ Cannot delete `{name}`.\nOnly plugins  `INSTALLED` can be removed."
            )
            return

        try:
            os.remove(plugin_path)
            await event.reply(f"✅ Plugin `{name}` removed.\nReboot bot to apply changes.")
        except Exception as e:
            await event.reply(f"❌ Error removing plugin:\n`{e}`")
