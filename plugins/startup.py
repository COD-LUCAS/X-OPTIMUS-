from telethon import events
from datetime import datetime

def build_ui(user):
    time_now = datetime.now().strftime("%I:%M %p")
    
    return f"""
╔══ 🔱 **X-OPTIMUS SYSTEM ONLINE** 🔱 ══╗

👤 **User**        : {user.first_name}
💠 **Mode**        : Active
⚡ **Power Core**  : Stable
🕒 **Time**        : {time_now}

📡 **Status Matrix:**
   ├─ CPU Sync        : ✔ Ready
   ├─ Network Link    : ✔ Connected
   └─ Core Engine     : ✔ Operational

🚀 **System Booted Successfully**  
Your commands are now active.
╚══════════════════════════════════╝
"""

async def on_startup(bot):
    user = await bot.get_me()
    message = build_ui(user)

    try:
        await bot.send_message("me", message)
    except:
        await bot.send_message("me", f"X-OPTIMUS started for {user.first_name}")


def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/startup$"))
    async def manual_start(event):
        user = await bot.get_me()
        await event.reply(build_ui(user))
