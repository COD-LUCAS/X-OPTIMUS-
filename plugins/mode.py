from telethon import events
import os

CONFIG_PATHS = [
    "container_data/config.env",
    "/home/container/container_data/config.env",
    "/home/container_data/config.env"
]

def save_mode(value):
    for path in CONFIG_PATHS:
        if os.path.exists(path):
            with open(path, "r") as f:
                lines = f.readlines()
            out = []
            found = False
            for x in lines:
                if x.startswith("MODE="):
                    out.append(f"MODE={value}\n")
                    found = True
                else:
                    out.append(x)
            if not found:
                out.append(f"MODE={value}\n")
            with open(path, "w") as f:
                f.writelines(out)
            return True
    return False


def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/mode(?:\s+(.*))?$"))
    async def mode_cmd(event):
        if str(event.sender_id) != str(event.client.owner_id):
            return await event.reply("❌ Only owner can change mode.")

        mode = event.pattern_match.group(1)
        if not mode:
            return await event.reply("Usage: /mode public | private")

        mode = mode.strip().upper()
        if mode not in ["PUBLIC", "PRIVATE"]:
            return await event.reply("❌ Mode must be PUBLIC or PRIVATE")

        if save_mode(mode):
            await event.reply(f"✅ Mode changed to **{mode}**\n🔄 Restart bot to apply.")
        else:
            await event.reply("❌ Failed to save mode.")
