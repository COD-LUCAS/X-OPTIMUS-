import requests
from telethon import events
from io import BytesIO

SEARCH_URL = "https://www.googleapis.com/customsearch/v1"
# FREE METHOD (no API key needed)
SCRAPE_URL = "https://www.google.com/search?tbm=isch&q={}"

def google_image_search(query, limit=5):
    """Scrapes Google Images (safe)."""
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    url = SCRAPE_URL.format(query.replace(" ", "+"))
    res = requests.get(url, headers=headers, timeout=10)

    if res.status_code != 200:
        return []

    results = []
    html = res.text.split('src="')

    for part in html[1:]:
        link = part.split('"')[0]
        if link.startswith("http") and "gstatic" not in link:
            results.append(link)
        if len(results) >= limit:
            break

    return results


def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/img(?:\s+(.*))?$"))
    async def img_search(event):
        query = event.pattern_match.group(1)

        if not query:
            return await event.reply("📌 **Usage:** `/img cat,5`\nSearches Google Images.")

        # Extract query and count
        parts = query.split(",")
        search_term = parts[0].strip()
        count = 5

        if len(parts) > 1:
            try:
                count = int(parts[1].strip())
            except:
                pass

        msg = await event.reply(f"🔍 Searching **{count} images** for: `{search_term}` ...")

        results = google_image_search(search_term, limit=count + 3)

        if not results:
            return await msg.edit("❌ No results found.")

        sent = 0

        for link in results:
            if sent >= count:
                break
            try:
                img = requests.get(link, timeout=10).content
                file = BytesIO(img)
                file.name = "image.jpg"
                await bot.send_file(event.chat_id, file, caption=f"🔎 `{search_term}`")
                sent += 1
            except:
                pass

        if sent == 0:
            return await msg.edit("❌ Failed to download images.")

        await msg.edit(f"✅ Sent **{sent}/{count}** images for `{search_term}`")
