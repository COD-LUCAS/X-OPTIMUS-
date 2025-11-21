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

    @bot.on(events.NewMessage(pattern=r"^/(setvar|delvar)(.*)"))
    async def env_handler(event):
        sender = event.sender_id

        # OWNER only
        owner = os.getenv("OWNER")
        if owner and str(sender) != owner:
            return await event.reply("❌ Only owner can use this command.")

        cmd = event.pattern_match.group(1)
        args = event.pattern_match.group(2).strip()

        config = find_config()
        if not config:
            return await event.reply("❌ config.env not found.")

        # ---------------------------
        #     SET VARIABLE
        # ---------------------------
        if cmd == "setvar":

            if "=" not in args:
                return await event.reply("❌ Invalid format.\nUse:\n`/setvar KEY=value`")

            key, value = args.split("=", 1)
            key = key.strip()
            value = value.strip()

            # Read file
            lines = []
            if os.path.exists(config):
                with open(config, "r") as f:
                    lines = f.read().splitlines()

            updated = False
            new_lines = []

            # Update if exists
            for line in lines:
                if line.startswith(f"{key}="):
                    new_lines.append(f"{key}={value}")
                    updated = True
                else:
                    new_lines.append(line)

            if not updated:
                new_lines.append(f"{key}={value}")

            # Write back
            with open(config, "w") as f:
                f.write("\n".join(new_lines))

            return await event.reply(
                f"✅ `{key}` updated successfully!\nRestart bot to apply."
            )

        # ---------------------------
        #     DELETE VARIABLE
        # ---------------------------
        if cmd == "delvar":

            key = args.strip()
            if not key:
                return await event.reply("❌ Usage: `/delvar KEY`")

            if not os.path.exists(config):
                return await event.reply("❌ config.env missing.")

            new_lines = []
            removed = False

            with open(config, "r") as f:
                for line in f:
                    if line.startswith(f"{key}="):
                        removed = True
                    else:
                        new_lines.append(line)

            with open(config, "w") as f:
                f.write("\n".join(new_lines))

            if removed:
                return await event.reply(f"🗑️ `{key}` removed.\nRestart bot.")
            else:
                return await event.reply("❌ Key not found.")
