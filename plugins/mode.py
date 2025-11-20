from telethon import events
import os

CONFIG = "container_data/config.env"

def get_mode():
    if not os.path.exists(CONFIG):
        return "PUBLIC"
    with open(CONFIG, "r") as f:
        for x in f.readlines():
            if x.startswith("MODE="):
                return x.replace("MODE=", "").strip()
    return "PUBLIC"

def set_mode(m):
    lines = []
    if os.path.exists(CONFIG):
        with open(CONFIG, "r") as f:
            lines = f.readlines()
    out = []
    found = False
    for x in lines:
        if x.startswith("MODE="):
            out.append(f"MODE={m}\n")
            found = True
        else:
            out.append(x)
    if not found:
        out.append(f"MODE={m}\n")
    with open(CONFIG, "w") as f:
        f.writelines(out)

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/mode(?:\s+(.*))?$"))
    async def mode_cmd(event):
        if str(event.sender_id) != str(event.client.owner_id):
            return

        arg = event.pattern_match.group(1)
        if not arg:
            return await event.reply(f"Current Mode: **{get_mode()}**\nUse `/mode public` or `/mode private`")

        arg = arg.upper()
        if arg not in ["PUBLIC", "PRIVATE"]:
            return await event.reply("Use: `/mode public` or `/mode private`")

        set_mode(arg)
        await event.reply(f"Mode changed to **{arg}**\nRestart bot.")
