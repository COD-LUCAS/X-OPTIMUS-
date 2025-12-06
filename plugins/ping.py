from telethon import events
import time

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/ping$"))
    async def ping(event):

        uid = event.sender_id
        mode = bot.mode.lower()

        if mode == "private":
            if uid != bot.owner_id and uid not in bot.sudo_users:
                return

        start = time.time()
        msg = await event.reply("Pinging...")
        end = time.time()

        ping_time = round((end - start) * 1000, 2)

        await msg.edit(f"Response time: {ping_time} ms")
