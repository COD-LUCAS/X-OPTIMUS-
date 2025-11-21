import requests
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/img\s+(.+)"))
    async def img_search(event):
        query = event.pattern_match.group(1).strip()

        if not query:
            return await event.reply("❌ Usage: `/img cat`")

        await event.reply(f"🔍 Searching images for **{query}** ...")

        try:
            url = f"https://bing-image-search-api.vercel.app/api?q={query}"
            r = requests.get(url, timeout=8)

            if r.status_code != 200:
                return await event.reply("❌ Error fetching images.")

            data = r.json()

            if "results" not in data or len(data["results"]) == 0:
                return await event.reply("❌ No images found.")

            count = 3
            results = data["results"][:count]

            for img in results:
                try:
                    await bot.send_file(event.chat_id, img["url"], caption=f"Image for: {query}")
                except:
                    pass

        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
