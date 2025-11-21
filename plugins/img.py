import requests
from bs4 import BeautifulSoup
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/img(?:\s+(.*))?$"))
    async def image_search(event):

        text = event.pattern_match.group(1)
        if not text:
            return await event.reply(
                "❌ Usage:\n"
                "`/img cat`\n"
                "`/img 5 dog`"
            )

        parts = text.split()
        limit = 3

        if parts[0].isdigit():
            limit = int(parts[0])
            limit = max(1, min(limit, 10))
            query = " ".join(parts[1:])
        else:
            query = text

        if not query:
            return await event.reply("❌ Provide a search term.")

        msg = await event.reply(f"🔍 Searching images for **{query}** ...")

        try:
            url = f"https://www.bing.com/images/search?q={query.replace(' ', '+')}&form=HDRSC2"
            html = requests.get(url, timeout=10).text
            soup = BeautifulSoup(html, "html.parser")
            images = soup.find_all("img")

            image_urls = []
            for img in images:
                src = img.get("src")
                if src and ("http" in src) and (".jpg" in src or ".png" in src):
                    image_urls.append(src)

                if len(image_urls) >= limit:
                    break

            if not image_urls:
                return await msg.edit("❌ No images found.")

            await msg.edit(f"📸 Sending {len(image_urls)} images for **{query}** ...")

            for i, img_url in enumerate(image_urls, start=1):
                try:
                    await bot.send_file(
                        event.chat_id,
                        img_url,
                        caption=f"{query} • {i}/{len(image_urls)}"
                    )
                except:
                    pass

            await msg.delete()

        except Exception as e:
            await msg.edit(f"❌ Error: {e}")
