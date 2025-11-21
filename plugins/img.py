import requests
from telethon import events

API = "https://lexica-q6kr.onrender.com/search?q="   # stable API

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/img\s*(.*)"))
    async def img_search(event):
        query = event.pattern_match.group(1).strip()

        if not query:
            return await event.reply(
                "❌ **Usage:** `/img <search term>`\nExample: `/img cat`"
            )

        msg = await event.reply(f"🔍 Searching images for **{query}** ...")

        try:
            r = requests.get(API + query, timeout=10)

            if r.status_code != 200:
                return await msg.edit("❌ API error. Try again later.")

            try:
                data = r.json()
            except:
                return await msg.edit("❌ Could not read images. (Invalid JSON)")

            if not data or "images" not in data or len(data["images"]) == 0:
                return await msg.edit("❌ No images found.")

            results = data["images"][:3]  # top 3 images

            for img in results:
                try:
                    await bot.send_file(event.chat_id, img["src"], caption=query)
                except:
                    pass

            await msg.delete()

        except Exception as e:
            await msg.edit(f"❌ Error: {str(e)}")
