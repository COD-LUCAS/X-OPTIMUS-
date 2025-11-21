import os
from telethon import events

CONFIG_PATHS = [
    "container_data/config.env",
    "/home/container/container_data/config.env",
]

def find_config():
    for p in CONFIG_PATHS:
        if os.path.exists(p):
            return p
    return None


def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/setvar (.+)"))
    async def set_var(event):
        data = event.pattern_match.group(1)

        if "=" not in data:
            return await event.reply("❌ Invalid format.\nUse:\n`/setvar KEY=value`")

        key, value = data.split("=", 1)
        key = key.strip()
        value = value.strip()

        config = find_config()
        if not config:
            return await event.reply("❌ config.env not found.")

        lines = []
        if os.path.exists(config):
            with open(config, "r") as f:
                lines = f.read().splitlines()

        updated = False
        new_lines = []

        for line in lines:
            if line.startswith(f"{key}="):
                new_lines.append(f"{key}={value}")
                updated = True
            else:
                new_lines.append(line)

        if not updated:
            new_lines.append(f"{key}={value}")

        with open(config, "w") as f:
            f.write("\n".join(new_lines))

        await event.reply(f"✅ `{key}` updated successfully!\nRestart bot to apply.")

    @bot.on(events.NewMessage(pattern=r"^/delvar (.+)"))
    async def del_var(event):
        key = event.pattern_match.group(1).strip()

        config = find_config()
        if not config:
            return await event.reply("❌ config.env not found.")

        if not os.path.exists(config):
            return await event.reply("❌ config.env does not exist.")

        new_lines = []
        removed = False

        with open(config, "r") as f:
            for line in f:
                if line.startswith(f"{key}="):
                    removed = True
                else:
                    new_lines.append(line.strip())

        with open(config, "w") as f:
            f.write("\n".join(new_lines))

        if removed:
            await event.reply(f"🗑️ `{key}` removed.\nRestart bot to apply.")
        else:
            await event.reply("❌ Key not found.")
