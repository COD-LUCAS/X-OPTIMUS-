from telethon import events
from telethon.tl.functions.users import GetFullUserRequest

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/id(?:\s+(.*))?$"))
    async def user_id(event):
        target = event.pattern_match.group(1)

        if event.is_reply and not target:
            replied = await event.get_reply_message()
            user = await bot(GetFullUserRequest(replied.sender_id))
        else:
            if not target:
                return await event.reply("Usage: /id @user | user_id | reply")
            try:
                try:
                    user = await bot(GetFullUserRequest(int(target)))
                except:
                    user = await bot(GetFullUserRequest(target))
            except:
                return await event.reply("User not found.")

        u = user.user
        out = f"**USER INFO**\n\n"
        out += f"ID: `{u.id}`\n"
        out += f"Access Hash: `{u.access_hash}`\n"
        if u.username:
            out += f"Username: @{u.username}\n"
        if u.phone:
            out += f"Phone: `{u.phone}`\n"

        await event.reply(out)
