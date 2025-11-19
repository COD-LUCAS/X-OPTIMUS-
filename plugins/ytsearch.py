from telethon import events
import requests

API = "https://api-aswin-sparky.koyeb.app/api/search/youtube?query={}"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/ytsearch ?(.*)"))
    async def ytsearch(event):

        query = event.pattern_match.group(1).strip()

        if not query:
            return await event.reply("❗ Give a search term.\nExample: `/ytsearch Alan Walker`")

        msg = await event.reply("🔎 Searching YouTube...")

        try:
            r = requests.get(API.format(query))
            data = r.json()

            if not data.get("status") or "results" not in data:
                return await msg.edit("❌ No results found.")

            results = data["results"][:10]

            text = f"**🔎 YouTube Search Results for:** `{query}`\n\n"

            for i, v in enumerate(results, start=1):
                title = v.get("title", "Unknown title")
                url = v.get("url", "No link")
                duration = v.get("duration", "N/A")
                channel = v.get("channel", "N/A")

                text += f"**{i}. {title}**\n"
                text += f"🕒 {duration}\n👤 {channel}\n🔗 {url}\n\n"

            await msg.edit(text)

        except Exception as e:
            await msg.edit(f"❌ Error: {e}")
