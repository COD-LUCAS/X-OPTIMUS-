import requests
from telethon import events
import io

PICSUM = "https://picsum.photos/600/400"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/img ?(.*)"))
    async def img(event):
        query = event.pattern_match.group(1).strip() or "random"

        msg = await event.reply("🖼️ Fetching image...")

        try:
            # picsum ignores query, but we use it for caption
            r = requests.get(PICSUM, stream=True, timeout=15)
            r.raise_for_status()

            image_bytes = io.BytesIO(r.content)
            image_bytes.name = f"{query}.jpg"

            await bot.send_file(
                event.chat_id,
                image_bytes,
                caption=f"📷 **Random Image**\n🔍 Query: {query}"
            )

            await msg.delete()

        except Exception as e:
            await msg.edit(f"❌ Error fetching image.\n`{e}`")
