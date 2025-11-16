from telethon import events, __version__
import time
import psutil
import platform

def register(bot):

    @bot.on(events.NewMessage(pattern="/ping"))
    async def ping(event):
        start = time.time()
        msg = await event.reply("Pinging…")
        end = time.time()

        ping_ms = int((end - start) * 1000)
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        system = platform.system()
        release = platform.release()
        uptime = int(time.time() - psutil.boot_time())

        hours = uptime // 3600
        minutes = (uptime % 3600) // 60

        caption = f"""
🏓 **Pong:** `{ping_ms} ms`
🖥 CPU: `{cpu}%`
💾 RAM: `{ram}%`
🕒 Uptime: `{hours}h {minutes}m`
⚙ OS: `{system} {release}`
📚 Telethon: `{__version__}`
"""

        await msg.delete()
        await bot.send_file(event.chat_id, "assets/ping.jpg", caption=caption)
