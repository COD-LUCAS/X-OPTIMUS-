from telethon import events
import asyncio

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/broadcast\s+(.+)"))
    async def broadcast(event):

        if not event.is_reply:
            return await event.reply("Reply to a message.\nUsage: /broadcast id1,id2,id3")

        ids = [i.strip() for i in event.pattern_match.group(1).split(",")]
        msg = await event.get_reply_message()

        sent = 0
        failed = 0
        failed_ids = []

        status = await event.reply("📢 Starting broadcast...")

        for uid in ids:
            try:
                entity = await bot.get_entity(int(uid))
                await bot.send_message(entity, msg)
                sent += 1
            except:
                failed += 1
                failed_ids.append(uid)
            await asyncio.sleep(0.4)

        text = f"📢 **Broadcast Completed**\n✔ Sent: {sent}\n❌ Failed: {failed}"

        if failed_ids:
            text += "\n\nFailed:\n" + "\n".join(failed_ids)

        await status.edit(text)
