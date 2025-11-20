from telethon import events
import requests
import re
import os

API_URL = "https://api-aswin-sparky.koyeb.app/api/downloader/ig?url="

def register(bot):

    @bot.on(events.NewMessage(pattern=None))
    async def autoinsta(event):
        try:
            if not event.raw_text:
                return

            text = event.raw_text.strip()

            # Detect Instagram URLs
            urls = re.findall(r'https?://[^\s]+', text)
            insta_links = [u for u in urls if "instagram.com" in u or "ig.me" in u]

            if not insta_links:
                return

            # React loading
            try:
                await event.react("⏳")
            except:
                pass

            for url in insta_links:
                await download_and_send(bot, event, url)

            # React success
            try:
                await event.react("✅")
            except:
                pass

        except Exception as e:
            try:
                await event.react("❌")
            except:
                pass
            print("AutoInsta Error:", e)


async def download_and_send(bot, event, url):
    try:
        api = API_URL + url
        response = requests.get(api, timeout=20).json()

        if not response.get("status"):
            await event.reply("❌ Error downloading media.")
            return

        media_list = response.get("data", [])

        if not media_list:
            await event.reply("❌ No media found.")
            return

        for media in media_list:
            file_url = media.get("url")

            if not file_url:
                continue

            # Detect file type
            if file_url.endswith(".mp4"):
                await bot.send_file(event.chat_id, file_url, caption="")
            else:
                await bot.send_file(event.chat_id, file_url, caption="")

    except Exception as e:
        print("Download Error:", e)
        await event.reply("❌ Failed to download Instagram media.")
