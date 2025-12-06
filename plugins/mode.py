import os
from telethon import events

CONFIG = "container_data/config.env"

def get_mode():
    mode = "PUBLIC"
    if os.path.exists(CONFIG):
        with open(CONFIG, "r") as f:
            for line in f.readlines():
                if line.startswith("MODE="):
                    mode = line.replace("MODE=", "").strip().upper()
    return mode

def set_mode(mode):
    lines = []
    found = False
    if os.path.exists(CONFIG):
        with open(CONFIG, "r") as f:
            lines = f.readlines()
    new_lines = []
    for line in lines:
        if line.startswith("MODE="):
            new_lines.append(f"MODE={mode}\n")
            found = True
        else:
            new_lines.append(line)
    if not found:
        new_lines.append(f"MODE={mode}\n")
    with open(CONFIG, "w") as f:
        f.writelines(new_lines)

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/mode(?:\s+(.*))?$"))
    async def mode_cmd(event):

        uid = event.sender_id
        if uid != bot.owner_id and uid not in bot.sudo_users:
            return await event.reply("❌ Permission denied.")

        arg = event.pattern_match.group(1)

        if not arg:
            return await event.reply(
                f"🔧 **Current Mode:** `{get_mode()}`\n\n"
                "Use:\n"
                "`/mode public`\n"
                "`/mode private`"
            )

        mode = arg.strip().upper()

        if mode not in ["PUBLIC", "PRIVATE"]:
            return await event.reply("❌ Invalid mode.\nUse: `/mode public` or `/mode private`")

        set_mode(mode)

        await event.reply(f"✅ **Mode changed to {mode}**\n🔄 Reboot bot to apply changes.")
