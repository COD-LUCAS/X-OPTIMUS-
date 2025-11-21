import requests
from bs4 import BeautifulSoup
from telethon import events

def google_images(query, limit=5):
    url = f"https://www.google.com/search?q={query}&tbm=isch"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    images = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if src and src.startswith("http"):
            images.append(src)

        if len(images) >= limit:
            break

    return images


def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/img(?:\s+(.*))?$"))
    async def google_img(event):

        text = event.pattern_match.group(1)

        if not text:
            return await event.reply("❌ Usage: `/img cat`\nOr `/img 5 car`")

        parts = text.split()
        if parts[0].isdigit():
            limit = int(parts[0])
            query = " ".join(parts[1:])
        else:
            limit = 3
            query = text

        loading = await event.reply(f"🔍 Searching `{query}`…")

        try:
            results = google_images(query, limit)

            if not results:
                return await loading.edit("❌ No images found.")

            await loading.edit(f"📸 Sending {len(results)} images…")

            for link in results:
                try:
                    await bot.send_file(event.chat_id, link)
                except:
                    pass

        except Exception as e:
            await loading.edit(f"⚠ Error:\n`{e}`")a
