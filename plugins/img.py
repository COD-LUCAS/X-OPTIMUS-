import requests
from telethon import events

API = "https://gurubotapi.vercel.app/googleimg?search="

def get_images(query):
    try:
        r = requests.get(API + query, timeout=10)
        data = r.json()
        return data.get("results", [])
    except:
        return []


def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/img ?(.*)"))
    async def img_search(event):
        text = event.pattern_match.group(1).strip()

        if not text:
            return await event.reply("Example:\n`/img cat`\n`/img 5 car`")

        # Default limit = 3
        limit = 3
        parts = text.split()

        if parts[0].isdigit():
            limit = int(parts[0])
            text = " ".join(parts[1:])

        if not text:
            return await event.reply("❌ Provide a valid search term.")

        msg = await event.reply(f"🔍 Searching **{text}**...")

        images = get_images(text)

        if not images:
            return await msg.edit("❌ No images found for that query.")

        limit = min(limit, len(images))

        await msg.edit(f"📥 Sending **{limit} images** for **{text}**...")

        for i in range(limit):
            try:
                await bot.send_file(event.chat_id, images[i], caption=f"{text} • {i+1}/{limit}")
            except:
                pass

        await msg.delete()
