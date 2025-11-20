from telethon import events
import os

CONFIG_PATHS = [
    "container_data/config.env",
    "/home/container/container_data/config.env"
]

def find_config():
    for p in CONFIG_PATHS:
        if os.path.exists(p):
            return p
    return None

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/mode ?(.*)"))
    async def mode(event):

        if str(event.sender_id) != event.client.owner:
            return

        new = event.pattern_match.group(1).strip().upper()

        if new not in ["PUBLIC", "PRIVATE"]:
            return await event.reply("❌ Modes: PUBLIC / PRIVATE")

        config_path = find_config()
        if not config_path:
            return await event.reply("❌ config.env not found!")

        with open(config_path, "r") as f:
            lines = f.readlines()

        out = []
        replaced = False

        for line in lines:
            if line.startswith("MODE="):
                out.append(f"MODE={new}\n")
                replaced = True
            else:
                out.append(line)

        if not replaced:
            out.append(f"MODE={new}\n")

        with open(config_path, "w") as f:
            f.writelines(out)

        await event.reply(f"✅ Mode changed to **{new}**.\n🔄 Restart bot.")
