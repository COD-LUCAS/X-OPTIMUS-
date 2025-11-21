import requests
from telethon import events

API = "https://duckduckgo.com/i.js?l=us-en&o=json&q="

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/img (.+)"))
    async def img(event):
        query = event.pattern_match.group(1).strip()

        msg = await event.reply("🔎 Searching images…")

        try:
            r = requests.get(API + query, headers={
                "User-Agent": "Mozilla/5.0"
            }, timeout=10).json()

            results = r.get("results", [])
            if not results:
                return await msg.edit("❌ No images found.")

            # get first real result
            img_url = results[0].get("image")

            if not img_url:
                return await msg.edit("❌ Image URL not found.")

            await bot.send_file(
                event.chat_id,
                img_url,
                caption=f"📷 **Image Result**\n🔍 Query: {query}",
                reply_to=event.id
            )

            await msg.delete()

        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
