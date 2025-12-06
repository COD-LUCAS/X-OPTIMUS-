from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/id(?:\s+(.*))?$"))
    async def user_id(event):

        mode = bot.mode.lower()
        uid = event.sender_id

        if mode == "private":
            if uid != bot.owner_id and uid not in bot.sudo_users:
                return await event.reply("❌ Private mode: only owner or sudo can use this command.")

        target = event.pattern_match.group(1)

        try:
            if event.is_reply and not target:
                msg = await event.get_reply_message()
                entity = await msg.get_sender()
            else:
                if not target:
                    return await event.reply("Usage: `/id @user`, `/id user_id`, or reply to a user.")

                t = target.strip()
                try:
                    entity = await bot.get_entity(int(t))
                except ValueError:
                    entity = await bot.get_entity(t)

            u = entity

            out = "🧾 **USER INFORMATION**\n"
            out += "━━━━━━━━━━━━━━━━━━\n"
            out += f"🆔 **ID:** `{u.id}`\n"
            out += f"🔐 **Access Hash:** `{getattr(u, 'access_hash', 'N/A')}`\n"
            out += f"👤 **First Name:** `{u.first_name or 'N/A'}`\n"
            out += f"👥 **Last Name:** `{u.last_name or 'N/A'}`\n"
            out += f"📛 **Username:** @{u.username}\n" if u.username else ""
            out += f"📱 **Phone:** `{u.phone}`\n" if u.phone else ""
            out += f"💬 **Bot:** `{u.bot}`\n"
            out += f"🚫 **Restricted:** `{u.restricted}`\n"
            out += f"⚠ **Scam:** `{u.scam}`\n"
            out += f"⭐ **Verified:** `{u.verified}`\n"
            out += "━━━━━━━━━━━━━━━━━━"

            try:
                photo = await bot.download_profile_photo(u, file="user_dp.jpg")
                if photo:
                    await bot.send_file(event.chat_id, photo, caption=out)
                    return
            except:
                pass

            await event.reply(out)

        except Exception as e:
            await event.reply(f"❌ Error fetching user info:\n`{e}`")
