from telethon import events
import os

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/remove (.+)$"))
    async def remove(event):
        name = event.pattern_match.group(1).strip()
        if not name.endswith(".py"):
            name += ".py"
        path = f"plugins/user_plugins/{name}"

        if not os.path.exists(path):
            return await event.reply("❌ Plugin not found.")

        os.remove(path)
        await event.reply(f"🗑 `{name}` removed.\nRestart to apply.")
