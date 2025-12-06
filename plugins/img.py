from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/img(?:\s+(.*))?$"))
    async def img_search(event):

        mode = bot.mode.lower()
        uid = event.sender_id

        # MODE = private → only owner or sudo can use
        if mode == "private":
            if uid != bot.owner_id and uid not in bot.sudo_users:
                return await event.reply("❌ Private mode: only owner or sudo can use this command.")

        await event.reply("⚙️ This feature is currently being worked on.\nPlease wait for the next update.")
