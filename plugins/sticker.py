from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/sticker$"))
    async def sticker_help(event):
        await event.reply(
            "**Sticker Commands:**\n"
            "/sticker — convert photo to sticker\n"
            "/sinfo — show sticker ID when sticker is sent\n"
        )

    @bot.on(events.NewMessage(pattern=r"^/sticker$", func=lambda e: e.is_reply))
    async def make_sticker(event):
        reply = await event.get_reply_message()
        
        if not reply.photo and not reply.document:
            return await event.reply("Reply to an **image**.")

        file = await reply.download_media()

        await event.reply("Making sticker…")

        try:
            await bot.send_file(
                event.chat_id,
                file,
                force_document=False,
                reply_to=event.id,
                attributes=[],
                mime_type="image/webp",
            )
            await event.reply("✅ **Sticker Created!**\nUse /sinfo to get sticker ID.")
        except Exception as e:
            await event.reply(f"❌ Failed to make sticker:\n`{e}`")

    @bot.on(events.NewMessage(pattern=r"^/sinfo$"))
    async def sticker_info(event):
        if not event.is_reply:
            return await event.reply("Reply to a **sticker**.")

        msg = await event.get_reply_message()
        
        if not msg.sticker:
            return await event.reply("Reply to a **sticker only**.")

        sticker = msg.sticker
        info = f"""
**Sticker Info**
🆔 ID: `{sticker.id}`
📦 Set ID: `{sticker.set_id}`
🔢 Emoji: `{sticker.attribute.emoji if sticker.attributes else 'N/A'}`
"""
        await event.reply(info)
