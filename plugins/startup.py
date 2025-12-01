from telethon import events
import os
from datetime import datetime

STARTUP_IMAGE = "assets/startup.jpg"

async def on_startup(bot):
    """
    Runs automatically on startup
    """
    user = await bot.get_me()
    time_now = datetime.now().strftime("%I:%M %p")

    caption = f"""
**X-OPTIMUS**

User: {user.first_name}
Status: Online
Time: {time_now}

Ready to use ✓
"""

    try:
        if os.path.exists(STARTUP_IMAGE):
            await bot.send_file("me", STARTUP_IMAGE, caption=caption)
        else:
            await bot.send_message("me", caption)
    except:
        await bot.send_message("me", f"X-OPTIMUS started for {user.first_name}")


def register(bot):
    """
    Manual startup command: /startup
    """
    @bot.on(events.NewMessage(pattern=r"^/startup$"))
    async def manual_start(event):
        user = await bot.get_me()
        
        status_msg = f"""
**Status Check**

Bot: Running
User: {user.first_name}
Response: Active
"""
        
        try:
            if os.path.exists(STARTUP_IMAGE):
                await event.reply(file=STARTUP_IMAGE, message=status_msg)
            else:
                await event.reply(status_msg)
        except:
            await event.reply("Bot is running ✓")
