import os
from telethon import events

CONFIG = "container_data/config.env"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/delvar\s+(.+)$"))
    async def del_var(event):
        if event.sender_id != bot.owner_id:
            return

        key = event.pattern_match.group(1).strip()

        if not key:
            return await event.reply("❌ Format: `/delvar KEY`")

        if not os.path.exists(CONFIG):
            return await event.reply("❌ config.env not found")

        lines = []
        removed = False

        with open(CONFIG, "r") as f:
            for line in f:
                if line.startswith(f"{key}="):
                    removed = True
                    continue
                lines.append(line)

        with open(CONFIG, "w") as f:
            f.writelines(lines)

        if removed:
            await event.reply(f"🗑 `{key}` removed.\nRestart bot.")
        else:
            await event.reply(f"⚠️ `{key}` not found.")
