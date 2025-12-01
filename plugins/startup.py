from telethon import events
import os
from datetime import datetime

STARTUP_IMAGE = "assets/startup.jpg"

async def on_startup(bot):
    """
    Runs automatically on startup via main.py's run_startup_events()
    """
    user = await bot.get_me()
    current_time = datetime.now().strftime("%I:%M %p")
    current_date = datetime.now().strftime("%B %d, %Y")

    caption = f"""
╔═══════════════════════════════╗
║   🌟 X-OPTIMUS INITIALIZED 🌟   ║
╚═══════════════════════════════╝

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 👤 **User**      ➜ {user.first_name}
┃ 🆔 **User ID**   ➜ `{user.id}`
┃ 📱 **Username**  ➜ @{user.username or 'N/A'}
┃ ⚙️  **Mode**      ➜ Userbot
┃ 🚀 **Status**    ➜ Online & Active
┃ 🕐 **Time**      ➜ {current_time}
┃ 📅 **Date**      ➜ {current_date}
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

✨ **All Systems Operational**
🔥 **Ready to Execute Commands**
💫 **Performance: Optimal**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Powered by Telethon
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    try:
        if os.path.exists(STARTUP_IMAGE):
            await bot.send_file("me", STARTUP_IMAGE, caption=caption)
        else:
            await bot.send_message("me", caption)
    except Exception as e:
        # Fallback simple message if formatting fails
        simple_msg = f"🟢 X-OPTIMUS Started!\n👤 User: {user.first_name}\n✅ Status: Online"
        await bot.send_message("me", simple_msg)


def register(bot):
    """
    Manual startup command: /startup
    """
    @bot.on(events.NewMessage(pattern=r"^/startup$"))
    async def manual_start(event):
        user = await bot.get_me()
        current_time = datetime.now().strftime("%I:%M %p")
        
        status_msg = f"""
╔═══════════════════════════════╗
║      🔥 STATUS CHECK 🔥        ║
╚═══════════════════════════════╝

✅ **Bot Status:** Running
👤 **User:** {user.first_name}
🕐 **Current Time:** {current_time}
⚡ **Response Time:** Instant
💚 **Health:** Excellent

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        try:
            if os.path.exists(STARTUP_IMAGE):
                await event.reply(file=STARTUP_IMAGE, message=status_msg)
            else:
                await event.reply(status_msg)
        except:
            await event.reply("🟢 Bot is running perfectly!")
