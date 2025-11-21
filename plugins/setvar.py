import os
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/setvar\s+(.+)"))
    async def set_var(event):
        if event.sender_id != bot.owner_id:
            return await event.reply("❌ Only owner can use this command.")

        data = event.pattern_match.group(1)

        if "=" not in data:
            return await event.reply("❌ Format: `/setvar KEY=value`")

        key, value = data.split("=", 1)
        key = key.strip()
        value = value.strip()

        config_path = "container_data/config.env"
        if not os.path.exists(config_path):
            open(config_path, "w").close()

        lines = []
        found = False

        with open(config_path, "r") as f:
            for line in f:
                if line.startswith(key + "="):
                    lines.append(f"{key}={value}\n")
                    found = True
                else:
                    lines.append(line)

        if not found:
            lines.append(f"{key}={value}\n")

        with open(config_path, "w") as f:
            f.writelines(lines)

        await event.reply(f"✅ `{key}` updated successfully.\n🔄 Restart bot to apply changes.")

    @bot.on(events.NewMessage(pattern=r"^/delvar\s+(.+)"))
    async def del_var(event):
        if event.sender_id != bot.owner_id:
            return await event.reply("❌ Only owner can use this command.")

        key = event.pattern_match.group(1).strip()

        config_path = "container_data/config.env"
        if not os.path.exists(config_path):
            return await event.reply("❌ No config.env file found.")

        lines = []
        removed = False

        with open(config_path, "r") as f:
            for line in f:
                if line.startswith(key + "="):
                    removed = True
                    continue
                lines.append(line)

        with open(config_path, "w") as f:
            f.writelines(lines)

        if removed:
            await event.reply(f"🗑 `{key}` removed.\n🔄 Restart bot to apply changes.")
        else:
            await event.reply("❌ Variable not found.")
