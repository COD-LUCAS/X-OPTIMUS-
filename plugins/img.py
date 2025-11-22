from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/img$"))
    async def img_temp(event):
        text = (
            "🖼 **Image Fetching Plugin Unavailable**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📌 The `/img` command is currently **under maintenance**.\n"
            "⚙️ We are improving it to make it *faster, smarter, and more accurate*.\n\n"
            "✨ **A brand-new upgraded version is coming soon!**\n"
            "Stay tuned…\n"
            "━━━━━━━━━━━━━━━━━━"
        )

        await event.reply(text)
