import requests

from telethon import events

API = "https://api.sparky.biz.id/api/downloader/igdl?url="

def register(bot):

    @bot.on(events.NewMessage(pattern=r"https?://(www\.)?instagram\.com/[^\s]+"))

    async def insta(event):

        url = event.pattern_match.group(0)

        status = await event.reply("📥 Downloading from Instagram…")

        try:

            res = requests.get(API + url).json()

            if not res.get("status"):

                return await status.edit("❌ Failed to download. Invalid or unsupported link.")

            count = 0

            for item in res.get("data", []):

                media = item.get("url")

                if not media:

                    continue

                count += 1

                if item.get("type") == "image":

                    await bot.send_file(event.chat_id, media, caption="", reply_to=event.id)

                elif item.get("type") == "video":

                    await bot.send_file(event.chat_id, media, caption="", reply_to=event.id)

                else:

                    await bot.send_file(event.chat_id, media, caption="", reply_to=event.id)

            await status.delete()

            if count == 0:

                await event.reply("⚠ No downloadable media found.")

            else:

                await event.reply(f"✅ Sent {count} media file(s).")

        except Exception as e:

            await status.edit(f"⚠ Error: {e}")
