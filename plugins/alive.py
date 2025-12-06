from telethon import events
import platform
import time

start_time = time.time()

def register(bot):

    @bot.on(events.NewMessage(pattern=r"/alive"))
    async def alive(event):

        mode = bot.mode.lower()
        uid = event.sender_id

        if mode == "private":
            if uid != bot.owner_id and uid not in bot.sudo_users:
                return await event.reply("❌ Private mode: access denied.")

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
