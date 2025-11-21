import requests
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/img(?:\s+(.*))?$"))
    async def img(event):
        query = event.pattern_match.group(1)

        # Simple loading message
        msg = await event.reply("📸 Fetching image...")

        try:
            # RANDOM IMAGE URL (No API, works always)
            img_url = "https://picsum.photos/800/600"

            # If user gives keyword → use a static google photo search redirect
            if query:
                img_url = f"https://source.unsplash.com/800x600/?{query}"

            # Download image
            r = requests.get(img_url, timeout=20)

            if r.status_code != 200:
                return await msg.edit("❌ Unable to fetch image.")

            # Save temp image
            file = "random_img.jpg"
            open(file, "wb").write(r.content)

            # Send image
            await bot.send_file(
                event.chat_id,
                file,
                caption=f"🖼 **Image Result**\n🔍 Query: `{query or 'random'}`"
            )

            await msg.delete()
            os.remove(file)

        except Exception as e:
            await msg.edit(f"❌ Error:\n`{e}`")
