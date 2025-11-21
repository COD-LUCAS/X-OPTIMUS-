import os
import asyncio
import subprocess
from telethon import events

TEMP_DIR = "container_data/temp_mp3"

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR, exist_ok=True)

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/mp3$"))
    async def extract_mp3(event):

        if not event.is_reply:
            return await event.reply("🎧 Reply to a **video** to extract audio.")

        reply = await event.get_reply_message()

        if not reply.video and not reply.document:
            return await event.reply("❌ Reply to a valid **video file**.")

        status = await event.reply("🎧 **Extracting audio…**")

        try:
            # download video to temp file
            video_path = f"{TEMP_DIR}/input_{event.id}.mp4"
            mp3_path = f"{TEMP_DIR}/output_{event.id}.mp3"

            await reply.download_media(video_path)

            # Use ffmpeg (fastest possible)
            cmd = [
                "ffmpeg", "-i", video_path,
                "-vn", "-acodec", "mp3",
                "-ab", "128k",
                "-ar", "44100",
                "-y",
                mp3_path
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            await process.communicate()

            if not os.path.exists(mp3_path):
                return await status.edit("❌ Failed to convert audio.")

            await bot.send_file(
                event.chat_id,
                mp3_path,
                caption="🎵 **Here is your MP3!**"
            )

            await status.delete()

        except Exception as e:
            await status.edit(f"❌ Error:\n`{e}`")

        finally:
            # cleanup
            if os.path.exists(video_path): os.remove(video_path)
            if os.path.exists(mp3_path): os.remove(mp3_path)
