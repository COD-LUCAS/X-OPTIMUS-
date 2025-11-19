import requests
from telethon import events

API_SEARCH = "https://api-aswin-sparky.koyeb.app/api/search/youtube?query="

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/ytsearch (.+)"))
    async def ytsearch(event):
        query = event.pattern_match.group(1).strip()
        msg = await event.reply("🔎 Searching YouTube…")

        try:
            url = API_SEARCH + query.replace(" ", "+")
            r = requests.get(url, timeout=20).json()

            if "data" not in r or len(r["data"]) == 0:
                return await msg.edit("❌ No results found.")

            results = r["data"]
            text = "**🔍 YouTube Search Results:**\n\n"

            for item in results[:10]:
                title = item.get("title", "N/A")
                link = item.get("url", "N/A")
                duration = item.get("duration", "N/A")
                channel = item.get("channel", "N/A")

                text += f"🎬 **{title}**\n"
                text += f"📺 Channel: `{channel}`\n"
                text += f"⏱ Duration: `{duration}`\n"
                text += f"🔗 {link}\n\n"

            await msg.edit(text)

        except Exception as e:
            await msg.edit(f"❌ Error:\n`{e}`")
