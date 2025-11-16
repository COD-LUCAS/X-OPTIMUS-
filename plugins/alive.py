from telethon import events
import platform
import time

start_time = time.time()

def register(bot):

    @bot.on(events.NewMessage(pattern="/alive"))
    async def alive(event):
        uptime = int(time.time() - start_time)
        h = uptime // 3600
        m = (uptime % 3600) // 60

        caption = f"""
🤖 **X-OPTIMUS ONLINE**
━━━━━━━━━━━━━━
🕒 Uptime: `{h}h {m}m`
💽 System: `{platform.system()}`
🔧 Python: `{platform.python_version()}`
🛠 Owner: `@codlucas`
━━━━━━━━━━━━━━
"""

        await bot.send_file(event.chat_id, "assets/alive.jpg", caption=caption)
