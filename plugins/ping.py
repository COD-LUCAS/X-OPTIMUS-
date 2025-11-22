from telethon import events
import time

def register(bot):
    
    @bot.on(events.NewMessage(pattern=r"^/ping$"))
    async def ping(event):
        start = time.time()
        msg = await event.reply("Pinging...")
        end = time.time()
        
        ping_time = round((end - start) * 1000, 2)
        
        await msg.edit(f"Response time: {ping_time} ms")
