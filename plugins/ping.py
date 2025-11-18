import os
from telethon import events
from datetime import datetime
import time

PING_IMAGE = "assets/ping.jpg"

def register(bot):
    
    @bot.on(events.NewMessage(pattern=r"^/ping$"))
    async def ping(event):
        
        # Calculate response time
        start = datetime.now()
        start_time = time.time()
        
        # React with ping pong sticker
        try:
            await event.react("🏓")
        except:
            pass
        
        # Calculate latency
        end = datetime.now()
        end_time = time.time()
        
        ping_time = (end - start).total_seconds() * 1000
        response_time = (end_time - start_time) * 1000
        
        # Get uptime if available
        uptime_str = "Running"
        
        # Determine ping status
        if ping_time < 100:
            status = "Excellent"
            bar = "████████████ 100%"
        elif ping_time < 200:
            status = "Good"
            bar = "█████████░░░ 75%"
        elif ping_time < 400:
            status = "Fair"
            bar = "██████░░░░░░ 50%"
        else:
            status = "Slow"
            bar = "███░░░░░░░░░ 25%"
        
        # Create message
        text = f"""**PONG! 🏓**

╭─────────────────╮
│  **Connection Status**  │
╰─────────────────╯

**Latency:** `{ping_time:.2f}ms`
**Status:** `{status}`
**Speed:** {bar}

**Bot:** `Online`
**Uptime:** `{uptime_str}`

╭─────────────────╮
│  **Performance**   │
╰─────────────────╯

Response: `{response_time:.3f}ms`
"""
        
        # Send with image if available
        if os.path.exists(PING_IMAGE):
            await event.reply(
                file=PING_IMAGE,
                message=text
            )
        else:
            await event.reply(text)
