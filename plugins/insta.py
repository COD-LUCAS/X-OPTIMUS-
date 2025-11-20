from aiogram import types
import aiohttp

API_URL = "https://api.sparky.biz.id/api/downloader/igdl?url="

def register(dp):

    @dp.message_handler(commands=["insta"])
    async def insta_cmd(msg: types.Message):
        if len(msg.text.split()) < 2:
            return await msg.reply("âŒ Send Instagram link.\nExample:\n`/insta https://instagram.com/...`")

        url = msg.text.split()[1]
        status = await msg.reply("ðŸ“¥ Downloadingâ€¦")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_URL + url) as r:
                    data = await r.json()

            if not data.get("status"):
                return await status.edit_text("âŒ Invalid or unsupported Instagram link.")

            count = 0

            for item in data.get("data", []):
                media_url = item.get("url")

                if item.get("type") == "image":
                    await msg.answer_photo(media_url)
                else:
                    await msg.answer_video(media_url)

                count += 1

            if count == 0:
                await msg.reply("âš  No media found.")
            else:
                await msg.reply(f"âœ… Sent {count} file(s).")

        except Exception as e:
            await status.edit_text(f"âš  Error: {str(e)}")
