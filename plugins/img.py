import requests
from telethon import events

def google_search(query):
    url = "https://api.duckduckgo.com/?q={}&iax=images&ia=images".format(query)
    try:
        data = requests.get(url, timeout=10).json()
        results = []

        if "image_results" in data:
            for x in data["image_results"]:
                img = x.get("image", {}).get("url")
                if img:
                    results.append(img)

        return results
    except:
        return []


def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/img ?(.*)"))
    async def img_search(event):
        q = event.pattern_match.group(1).strip()

        if not q:
            return await event.reply("Example:\n`/img cat`\n`/img 5 car`")

        limit = 3
        parts = q.split()

        if parts[0].isdigit():
            limit = int(parts[0])
            q = " ".join(parts[1:])

        if not q:
            return await event.reply("❌ Provide a search term.")

        status = await event.reply(f"🔍 Searching images for **{q}**...")

        images = google_search(q)

        if not images:
            return await status.edit("❌ No images found.")

        limit = min(limit, len(images))

        await status.edit(f"📥 Downloading **{limit} images** for **{q}**...")

        for i in range(limit):
            try:
                await bot.send_file(event.chat_id, images[i], caption=f"Image {i+1}/{limit} • {q}")
            except:
                pass

        await status.delete()
