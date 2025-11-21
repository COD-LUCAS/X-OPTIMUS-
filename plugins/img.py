import requests
import os
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/img(?:\s+(.*))?$"))
    async def img(event):
        query = event.pattern_match.group(1)

        if not query:
            return await event.reply(
                "Please provide a search query.\nExample: `/img cat`"
            )

        msg = await event.reply(f"🔍 Searching images for: **{query}** ...")

        try:
            url = "https://duckduckgo.com/"
            token = requests.post(url, data={"q": query}).text.split("vqd=")[1].split("&")[0]

            api = (
                "https://duckduckgo.com/i.js?l=us-en&o=json"
                f"&q={query}&vqd={token}"
            )
            data = requests.get(api, headers={"User-Agent": "Mozilla/5.0"}).json()

            results = data.get("results", [])[:4]

            if not results:
                return await msg.edit("❌ No images found.")

            for item in results:
                img_url = item["image"]
                file = "img.jpg"

                r = requests.get(img_url, timeout=10)
                open(file, "wb").write(r.content)

                await bot.send_file(event.chat_id, file, caption=f"Image for: {query}")
                os.remove(file)

            await msg.delete()

        except Exception as e:
            await msg.edit(f"❌ Error: {str(e)}")
