from telethon import events
from datetime import datetime

def build_ui():
    return (
        "*_X-OPTIMUS STARTED!_* \n\n"
        "_Mode         :_ *Public*\n"
        "_Language     :_ *English*\n"
        "_Handlers     :_ *.,*\n"
        "_Status       :_ *Online*\n"
        "_Engine       :_ *Active*"
    )

async def on_startup(bot):
    try:
        await bot.send_message("me", build_ui())
    except:
        pass

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/startup$"))
    async def manual_start(event):
        await event.reply(build_ui())
