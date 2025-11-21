import os
import asyncio
from telethon import events
from moviepy.editor import VideoFileClip

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/mp3$"))
    async def convert_to_mp3(event):

        if not event.is_reply:
            return await event.reply("🎧 Reply to a video to extract audio.")

        reply = await event.get_reply_message()

        if not reply.video:
            return await event.reply("❌ This is not a video. Reply to a video.")

        msg = await event.reply("🎶 Extracting audio…")

        try:
            # Download video
            video_path = await reply.download_media(file="video.mp4")

            mp3_path = "output.mp3"

            # Convert to MP3 using moviepy
            clip = VideoFileClip(video_path)
            clip.audio.write_audiofile(mp3_path, codec="libmp3lame")
            clip.close()

            # Send audio file
            await bot.send_file(
                event.chat_id,
                mp3_path,
                caption="🎵 **Here is your MP3**",
                reply_to=event.id
            )

            await msg.delete()

        except Exception as e:
            await msg.edit(f"❌ Error:\n`{e}`")

        finally:
            # Cleanup
            try:
                if os.path.exists(video_path):
                    os.remove(video_path)
                if os.path.exists(mp3_path):
                    os.remove(mp3_path)
            except:
                pass
