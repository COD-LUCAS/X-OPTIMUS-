import os
import requests
from telethon import events

CATBOX_UPLOAD = "https://catbox.moe/user/api.php"

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/url$"))
    async def upload_to_catbox(event):

        uid = event.sender_id
        mode = bot.mode.lower()

        if mode == "private":
            if uid != bot.owner_id and uid not in bot.sudo_users:
                return

        if not event.is_reply:
            return await event.reply("📌 Reply `/url` to a media file (photo, video, audio, doc).")

        reply = await event.get_reply_message()

        if not reply.media:
            return await event.reply("❌ No media found! Reply to an image/video/document.")

        status = await event.reply("⬆️ Uploading to Catbox… Please wait.")

        try:
            file_path = await bot.download_media(reply, file="catbox_temp")

            if not file_path or not os.path.exists(file_path):
                return await status.edit("❌ Failed to download media.")

            files = {"fileToUpload": open(file_path, "rb")}
            data = {"reqtype": "fileupload"}

            upload = requests.post(CATBOX_UPLOAD, data=data, files=files, timeout=40)
            url = upload.text.strip()

            os.remove(file_path)

            if "catbox" not in url:
                return await status.edit("❌ Upload failed. Catbox returned an error.")

            await status.edit(f"✅ **Uploaded Successfully!**\n\n📎 **URL:**\n`{url}`")

        except Exception as e:
            await status.edit(f"❌ Error:\n`{e}`")
