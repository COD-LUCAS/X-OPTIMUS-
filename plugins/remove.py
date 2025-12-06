import os
from telethon import events

USER_DIR = "container_data/user_plugins"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/remove\s+(.+)"))
    async def remove_plugin(event):

        uid = event.sender_id

        if uid != bot.owner_id and uid not in bot.sudo_users:
            return await event.reply("❌ Permission denied.")

        name = event.pattern_match.group(1).strip()
        path = f"{USER_DIR}/{name}.py"

        if not os.path.exists(path):
            return await event.reply("❌ Plugin not found.")

        try:
            os.remove(path)
            await event.reply(
                f"🗑️ Plugin **{name}** removed.\n"
                f"🔄 Use `/reboot` to apply changes."
            )
        except Exception as e:
            await event.reply(f"❌ Failed to remove plugin:\n`{e}`")
