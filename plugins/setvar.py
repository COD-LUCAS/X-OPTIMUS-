import os
from telethon import events

CONFIG = "container_data/config.env"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/setvar\s+(.+)$"))
    async def set_var(event):
        if event.sender_id != bot.owner_id:
            return

        text = event.pattern_match.group(1).strip()

        if "=" not in text:
            return await event.reply("❌ Format: `/setvar KEY=VALUE`")

        key, value = text.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key or not value:
            return await event.reply("❌ Invalid format")

        if not os.path.exists(CONFIG):
            return await event.reply("❌ config.env not found")

        lines = []
        updated = False

        with open(CONFIG, "r") as f:
            for line in f:
                if line.startswith(f"{key}="):
                    lines.append(f"{key}={value}\n")
                    updated = True
                else:
                    lines.append(line)

        if not updated:
            lines.append(f"{key}={value}\n")

        with open(CONFIG, "w") as f:
            f.writelines(lines)

        await event.reply(f"✅ `{key}` updated successfully.\nReboot bot.")
