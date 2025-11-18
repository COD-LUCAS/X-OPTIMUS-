from telethon import events
import os

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/remove (.+)"))
    async def remove_plugin(event):
        name = event.pattern_match.group(1).strip()

        if not name.endswith(".py"):
            name = name + ".py"

        path = f"plugins/{name}"

        if not os.path.exists(path):
            return await event.reply(f"❌ Plugin `{name}` not found.")

        try:
            os.remove(path)
            await event.reply(f"🗑 Plugin `{name}` removed.\nRestart bot to apply changes.")
        except Exception as e:
            await event.reply(f"❌ Error removing plugin:\n`{e}`")
