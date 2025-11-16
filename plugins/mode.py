from telethon import events

def register(bot):
    @bot.on(events.NewMessage(pattern="/mode ?(.*)"))
    async def mode(event):
        if str(event.sender_id) != event.client.owner:
            return
        new = event.pattern_match.group(1).strip().upper()
        if new not in ["PUBLIC", "PRIVATE"]:
            await event.reply("Modes: PUBLIC / PRIVATE")
            return
        with open("config.env", "r") as f:
            lines = f.readlines()
        out = []
        for x in lines:
            if x.startswith("MODE="):
                out.append(f"MODE={new}\n")
            else:
                out.append(x)
        with open("config.env", "w") as f:
            f.writelines(out)
        await event.reply(f"Mode changed to **{new}**.\nRestart bot.")
