from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/id(?:\s+(.*))?$"))
    async def user_id(event):
        target = event.pattern_match.group(1)

        try:
            # 1) Reply case: /id as reply
            if event.is_reply and not target:
                msg = await event.get_reply_message()
                entity = await msg.get_sender()

            # 2) /id <something>
            else:
                if not target:
                    return await event.reply("Usage: /id @user | user_id | reply")

                t = target.strip()

                try:
                    entity = await bot.get_entity(int(t))
                except ValueError:
                    entity = await bot.get_entity(t)

            u = entity

            out = "**USER INFO**\n\n"
            out += f"ID: `{u.id}`\n"
            if getattr(u, 'access_hash', None) is not None:
                out += f"Access Hash: `{u.access_hash}`\n"
            if getattr(u, 'username', None):
                out += f"Username: @{u.username}\n"
            if getattr(u, 'phone', None):
                out += f"Phone: `{u.phone}`\n"
            if getattr(u, 'first_name', None):
                out += f"First Name: `{u.first_name}`\n"
            if getattr(u, 'last_name', None):
                out += f"Last Name: `{u.last_name}`\n"

            await event.reply(out or "No data found.")

        except Exception as e:
            await event.reply(f"❌ Failed to fetch user.\n`{e}`")
