import requests
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/img\s+(.+)"))
    async def img_search(event):
        query = event.pattern_match.group(1).strip()

        msg = await event.reply(f"🔍 Searching images for **{query}** ...")

        try:
            # DuckDuckGo working API
            response = requests.get(
                "https://duckduckgo-api.onrender.com/image",
                params={"q": query},
                timeout=20
            )

            if response.status_code != 200:
                return await msg.edit(f"❌ API Error:\n`{response.text}`")

            data = response.json()

            if not data or "results" not in data or len(data["results"]) == 0:
                return await msg.edit("❌ No images found. Try another keyword.")

            results = data["results"][:3]  # send 3 images

            await msg.edit(f"📸 Sending top {len(results)} results for **{query}**…")

            for img in results:
                url = img.get("image")
                if url:
                    await bot.send_file(event.chat_id, url, caption=f"Image for: {query}")

        except Exception as e:
            await msg.edit(f"❌ Error:\n`{e}`")
