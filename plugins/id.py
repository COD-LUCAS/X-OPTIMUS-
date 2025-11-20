from telethon import events
from telethon.tl.functions.users import GetFullUserRequest

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/id(?:\s+(.*))?$"))
    async def user_id(event):
        target = event.pattern_match.group(1)

        try:
            # Reply case
            if event.is_reply and not target:
                msg = await event.get_reply_message()
                entity = await bot.get_entity(msg.sender_id)

            else:
                if not target:
                    return await event.reply("Usage: /id @user | user_id | reply")
                try:
                    # Try numeric
                    entity = await bot.get_entity(int(target))
                except:
                    # Try username
                    entity = await bot.get_entity(target)

            full = await bot(GetFullUserRequest(entity.id))
            u = full.user

            out = "**USER INFO**\n\n"
            out += f"ID: `{u.id}`\n"
            out += f"Access Hash: `{u.access_hash}`\n"
            if u.username:
                out += f"Username: @{u.username}\n"
            if u.phone:
                out += f"Phone: `{u.phone}`\n"
            out += f"First Name: `{u.first_name}`\n"
            if u.last_name:
                out += f"Last Name: `{u.last_name}`\n"

            await event.reply(out)

        except Exception as e:
            await event.reply(f"❌ Failed to fetch user.\n`{e}`")
