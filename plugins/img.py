import requests
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/img\s+(.+)"))
    async def img(event):
        query = event.pattern_match.group(1).strip()
        msg = await event.reply(f"🔍 Searching images for **{query}** ...")

        try:
            # REAL DuckDuckGo API
            url = "https://duckduckgo.com/?q=" + query
            token_request = requests.get(url, timeout=10).text

            vqd = token_request.split("vqd=")[1].split("&")[0].replace("'", "")

            api_url = "https://duckduckgo.com/i.js"
            params = {"q": query, "vqd": vqd, "o": "json"}

            images = requests.get(api_url, params=params, timeout=10).json()

            if "results" not in images or len(images["results"]) == 0:
                return await msg.edit("❌ No images found.")

            results = images["results"][:3]

            await msg.edit(f"📸 Sending top {len(results)} results for **{query}**")

            for img in results:
                await bot.send_file(event.chat_id, img["image"], caption=f"Image for: {query}")

        except Exception as e:
            await msg.edit(f"❌ Error:\n`{e}`")
