import os
from telethon import events
from datetime import datetime
import time

PING_IMAGE = "assets/ping.jpg"

# Popular ping/pong sticker file_id (you can replace this with any sticker you like)
PING_STICKER_ID = "CAACAgIAAxkBAAEMYp5nO7RqLKZ8vPxU0z1hAAGxMGBBqwACShAAAtY3uEjqJqQ_UoH9fDYE"

def register(bot):
    
    @bot.on(events.NewMessage(pattern=r"^/ping$"))
    async def ping(event):
        
        # Calculate response time
        start = datetime.now()
        start_time = time.time()
        
        # Send sticker as reaction (reply to message with sticker)
        try:
            await bot.send_file(
                event.chat_id,
                PING_STICKER_ID,
                reply_to=event.id
            )
        except:
            # If sticker fails, use emoji reaction
            try:
                await event.react("🏓")
            except:
                pass
        
        # Calculate latency
        end = datetime.now()
        end_time = time.time()
        
        ping_time = (end - start).total_seconds() * 1000
        response_time = (end_time - start_time) * 1000
        
        # Determine ping status
        if ping_time < 100:
            status = "Excellent"
            emoji = "⚡"
        elif ping_time < 200:
            status = "Good"
            emoji = "✅"
        elif ping_time < 400:
            status = "Fair"
            emoji = "⚠️"
        else:
            status = "Slow"
            emoji = "🐌"
        
        # Create message
        text = f"""**Pong! 🏓**

**Latency:** `{ping_time:.2f} ms`
**Status:** {status} {emoji}
**Response:** `{response_time:.2f} ms`
"""
        
        # Send with image if available
        if os.path.exists(PING_IMAGE):
            await event.reply(
                file=PING_IMAGE,
                message=text
            )
        else:
            await event.reply(text)
