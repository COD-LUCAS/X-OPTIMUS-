import os
import time
from datetime import datetime
from telethon import events

PING_IMAGE = "assets/ping.jpg"


def register(bot):
    
    @bot.on(events.NewMessage(pattern=r"^/ping$"))
    async def ping(event):
        # Record start time
        start = time.time()
        
        # Send initial message
        msg = await event.reply("🏓 **Pinging...**")
        
        # Calculate ping time
        end = time.time()
        ping_time = (end - start) * 1000  # Convert to milliseconds
        
        # Get current time
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        # Create response text
        text = f"""
🤖 **X-OPTIMUS IS ALIVE!**

⚡ **Ping:** `{ping_time:.2f}ms`
🕐 **Time:** `{current_time}`
📅 **Date:** `{current_date}`
🟢 **Status:** Online

━━━━━━━━━━━━━━━━━━━━
🔥 **Bot is running smoothly!**
"""
        
        # Edit message with ping result
        if os.path.exists(PING_IMAGE):
            # Delete the "Pinging..." message
            await msg.delete()
            # Send new message with image
            await event.reply(
                file=PING_IMAGE,
                message=text
            )
        else:
            # Just edit the text if no image
            await msg.edit(text)
