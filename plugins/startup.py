from telethon import events
import os

STARTUP_IMAGE = "assets/startup.jpg"  # your image file

async def on_startup(bot):
    """
    This runs automatically on startup because main.py calls run_startup_events()
    """

    user = await bot.get_me()

    caption = f"""
🟢 **X-OPTIMUS Started Successfully!**

👤 **User:** {user.first_name}
⚙️ **System:** Userbot Online & Running
🚀 **Status:** Activated
"""

    # Send startup image if present
    if os.path.exists(STARTUP_IMAGE):
        await bot.send_file("me", STARTUP_IMAGE, caption=caption)
    else:
        await bot.send_message("me", caption)


def register(bot):
    """
    Optional manual command if user types /startup
    """
    @bot.on(events.NewMessage(pattern="/startup"))
    async def manual_start(event):
        if os.path.exists(STARTUP_IMAGE):
            await event.reply(file=STARTUP_IMAGE, message="🟢 Bot is running!")
        else:
            await event.reply("🟢 Bot is running!")
