import requests
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/img\s*(.*)"))
    async def img_search(event):
        query = event.pattern_match.group(1).strip()

        if not query:
            return await event.reply(
                "❌ **Usage:**\n`/img <search term>`\n\nExample:\n/img cat"
            )

        msg = await event.reply(f"🔍 Searching images for **{query}** ...")

        try:
            api = f"https://duckduckgo-image-api.vercel.app/search?query={query}"
            res = requests.get(api, timeout=10).json()

            if not res or "results" not in res or len(res["results"]) == 0:
                return await msg.edit("❌ No images found.")

            results = res["results"][:3]  # Send top 3 images

            for img in results:
                try:
                    await bot.send_file(event.chat_id, img["image"], caption=f"Image: {query}")
                except:
                    pass

            await msg.delete()

        except Exception as e:
            await msg.edit(f"❌ Error: {str(e)}")
