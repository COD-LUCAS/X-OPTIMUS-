import os
from telethon import events

USER_PLUGIN_DIR = "plugins/user_plugins"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/remove (.+)$"))
    async def remove_plugin(event):
        name = event.pattern_match.group(1).strip()

        # Ensure folder exists
        if not os.path.exists(USER_PLUGIN_DIR):
            os.makedirs(USER_PLUGIN_DIR)

        # Only allow deleting from user_plugins
        plugin_path = os.path.join(USER_PLUGIN_DIR, f"{name}.py")

        # Check if file exists
        if not os.path.isfile(plugin_path):
            await event.reply(
                f"❌ Cannot delete `{name}`.\n"
                f"Only plugins inside **plugins/user_plugins** can be removed."
            )
            return

        # Try deleting
        try:
            os.remove(plugin_path)
            await event.reply(f"✅ Plugin `{name}` removed.\nRestart bot to apply changes.")
        except Exception as e:
            await event.reply(f"❌ Error removing plugin:\n`{e}`")
