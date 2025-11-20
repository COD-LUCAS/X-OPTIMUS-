from telethon import events
from telethon.tl.functions.channels import InviteToChannelRequest
import asyncio

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/add\s+(.+)"))
    async def add(event):

        if event.is_private:
            return await event.reply("❌ Works only in groups.")

        ids = [i.strip() for i in event.pattern_match.group(1).split(",")]

        ok = 0
        fail = 0
        failed = []

        status = await event.reply("➕ Adding users...")

        for uid in ids:
            try:
                entity = await bot.get_entity(int(uid))
                await bot(InviteToChannelRequest(event.chat_id, [entity]))
                ok += 1
            except:
                fail += 1
                failed.append(uid)
            await asyncio.sleep(2)

        text = f"➕ **Add Users Completed**\n✔ Added: {ok}\n❌ Failed: {fail}"

        if failed:
            text += "\n\nFailed:\n" + "\n".join(failed)

        await status.edit(text)
