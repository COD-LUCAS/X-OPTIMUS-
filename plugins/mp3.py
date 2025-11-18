from telethon import events
import os
import subprocess

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/mp3$"))
    async def mp3_convert(event):
        reply = await event.get_reply_message()

        if not reply:
            return await event.reply("Reply to a video/audio/voice note.")

        msg = await event.reply("🔄 Converting to MP3...")

        try:
            downloaded = await bot.download_media(reply, file="input_media")

            output = "output.mp3"

            subprocess.run(
                ["ffmpeg", "-i", downloaded, "-vn", "-ab", "192k", "-ar", "44100", "-y", output],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            await event.reply("🎵 MP3 Ready!", file=output)
            await msg.delete()

            os.remove(downloaded)
            os.remove(output)

        except Exception as e:
            await msg.edit(f"❌ Conversion failed\n`{e}`")
