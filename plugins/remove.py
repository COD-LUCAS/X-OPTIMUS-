import os
from telethon import events

USER_DIR = "container_data/user_plugins"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/remove\s+(.+)"))
    async def remove_plugin(event):

        # OWNER CHECK
        if event.sender_id != bot.owner_id:
            return await event.reply("❌ Only owner can remove plugins.")

        name = event.pattern_match.group(1).strip()
        path = f"{USER_DIR}/{name}.py"

        if not os.path.exists(path):
            return await event.reply("❌ Plugin not found in installed plugins.")

        try:
            os.remove(path)
            await event.reply(
                f"🗑️ Plugin **{name}** removed.\n"
                f"🔄 Use `/reboot` to apply changes."
            )
        except Exception as e:
            await event.reply(f"❌ Failed to remove plugin:\n`{e}`")
