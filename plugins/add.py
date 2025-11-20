from telethon import events
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputPeerUser
import asyncio

def register(bot):

    async def resolve_user(bot, user_id):
        try:
            uid = int(user_id)
            full = await bot(GetFullUserRequest(uid))
            return InputPeerUser(full.user.id, full.user.access_hash)
        except:
            return None

    @bot.on(events.NewMessage(pattern=r"^/add(?:\s+(.*))?$"))
    async def add_users(event):
        if event.is_private:
            return await event.reply("Use in groups only.")
        query = event.pattern_match.group(1)
        if not query:
            return await event.reply("Usage: /add user_ids")
        ids = [x.strip() for x in query.split(",") if x.strip()]
        status = await event.reply(f"Adding {len(ids)} users…")
        success = 0
        failed = []
        for uid in ids:
            try:
                entity = await resolve_user(bot, uid)
                if not entity:
                    failed.append(f"{uid}")
                    continue
                await bot(InviteToChannelRequest(event.chat_id, [entity]))
                success += 1
                await asyncio.sleep(1.5)
            except Exception as e:
                failed.append(f"{uid}")
                await asyncio.sleep(1)
        out = f"✔ Added: {success}\n✖ Failed: {len(failed)}"
        if failed:
            out += "\n" + "\n".join(failed[:10])
        await status.edit(out)
