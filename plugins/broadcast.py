from telethon import events
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

    @bot.on(events.NewMessage(pattern=r"^/broadcast(?:\s+(.*))?$"))
    async def broadcast(event):
        query = event.pattern_match.group(1)
        if not query:
            return await event.reply("Usage: reply to message → /broadcast ids")
        if not event.is_reply:
            return await event.reply("Reply to a message first.")
        reply_msg = await event.get_reply_message()
        ids = [x.strip() for x in query.split(",") if x.strip()]
        status = await event.reply(f"Sending to {len(ids)} users…")
        success = 0
        failed = []
        for uid in ids:
            try:
                entity = await resolve_user(bot, uid)
                if not entity:
                    failed.append(uid)
                    continue
                await bot.send_message(entity, reply_msg)
                success += 1
                await asyncio.sleep(0.5)
            except:
                failed.append(uid)
                await asyncio.sleep(0.3)
        out = f"✔ Sent: {success}\n✖ Failed: {len(failed)}"
        if failed:
            out += "\n" + "\n".join(failed[:10])
        await status.edit(out)
