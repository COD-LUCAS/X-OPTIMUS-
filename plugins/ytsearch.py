from telethon import events
import requests

API = "https://widipe.com/search/youtube?query={}"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/ytsearch ?(.*)"))
    async def ytsearch(event):

        query = event.pattern_match.group(1).strip()

        if not query:
            return await event.reply("❗ Give something to search.\nExample: `/ytsearch alan walker`")

        msg = await event.reply("🔎 Searching...")

        try:
            r = requests.get(API.format(query))
            data = r.json()

            if "data" not in data or len(data["data"]) == 0:
                return await msg.edit("❌ No results found.")

            results = data["data"][:10]

            txt = f"**🔎 YouTube Search Results:** `{query}`\n\n"

            for i, v in enumerate(results, start=1):
                title = v.get("title")
                url = v.get("url")
                channel = v.get("channel")
                duration = v.get("duration")

                txt += f"**{i}. {title}**\n"
                txt += f"🕒 {duration}\n👤 {channel}\n🔗 {url}\n\n"

            await msg.edit(txt)

        except Exception as e:
            await msg.edit(f"❌ Error: {e}")
