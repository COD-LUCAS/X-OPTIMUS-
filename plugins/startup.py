import os
from telethon import events

def get_mode():
    # AUTO-DETECT MODE
    if os.getenv("PUBLIC_MODE") in ["False", "0", "false"]:
        return "Private"
    if os.getenv("OWNER_ONLY") in ["True", "1", "true"]:
        return "Private"
    return "Public"

def startup_text():
    mode = get_mode()

    return (
        "🔥 𝗫-𝗢𝗣𝗧𝗜𝗠𝗨𝗦 𝗢𝗡𝗟𝗜𝗡𝗘\n\n"
        f"▪ 𝗠𝗼𝗱𝗲       : {mode}\n"
        "▪ 𝗟𝗮𝗻𝗴𝘂𝗮𝗴𝗲   : 𝗘𝗻𝗴𝗹𝗶𝘀𝗵\n"
        "▪ 𝗦𝘁𝗮𝘁𝘂𝘀     : 𝗢𝗻𝗹𝗶𝗻𝗲\n"
        "▪ 𝗛𝗮𝗻𝗱𝗹𝗲𝗿𝘀   : 𝗟𝗼𝗮𝗱𝗲𝗱"
    )

async def on_startup(bot):
    try:
        await bot.send_message("me", startup_text())
    except:
        pass

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/startup$"))
    async def startup(event):
        await event.reply(startup_text())
