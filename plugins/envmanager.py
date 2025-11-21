import os
from telethon import events

CONFIG = "container_data/config.env"


def load_env():
    data = {}
    if os.path.exists(CONFIG):
        with open(CONFIG, "r") as f:
            for i in f:
                if "=" in i:
                    k, v = i.strip().split("=", 1)
                    data[k] = v
    return data


def save_env(data):
    with open(CONFIG, "w") as f:
        for k, v in data.items():
            f.write(f"{k}={v}\n")


def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/setvar\s*(.*)"))
    async def setvar(event):
        sender = await event.get_sender()
        if str(sender.id) != str(bot.owner_id):
            return await event.reply("❌ Only owner can use this command.")

        args = event.pattern_match.group(1).strip()

        if not args or "=" not in args:
            return await event.reply(
                "**Usage:**\n"
                "`/setvar KEY=value`\n"
                "Example:\n"
                "`/setvar REMOVE_BG_API_KEY=your_key_here`"
            )

        key, value = args.split("=", 1)
        data = load_env()
        data[key] = value
        save_env(data)

        await event.reply(f"✅ `{key}` updated successfully.")

    @bot.on(events.NewMessage(pattern=r"^/delvar\s*(.*)"))
    async def delvar(event):
        sender = await event.get_sender()
        if str(sender.id) != str(bot.owner_id):
            return await event.reply("❌ Only owner can use this command.")

        key = event.pattern_match.group(1).strip()

        if not key:
            return await event.reply(
                "**Usage:**\n"
                "`/delvar KEY`\n"
                "Example:\n"
                "`/delvar REMOVE_BG_API_KEY`"
            )

        data = load_env()

        if key in data:
            del data[key]
            save_env(data)
            return await event.reply(f"🗑️ `{key}` removed.")
        else:
            return await event.reply("❌ Variable not found.")
