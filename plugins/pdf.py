import os
import img2pdf
from telethon import events

PDF_TEMP = "container_data/pdf_temp"

def ensure_folder():
    if not os.path.exists(PDF_TEMP):
        os.makedirs(PDF_TEMP)

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/pdf$"))
    async def pdf_main(event):

        uid = event.sender_id
        mode = bot.mode.lower()
        if mode == "private":
            if uid != bot.owner_id and uid not in bot.sudo_users:
                return

        if not event.is_reply:
            return await event.reply(
                "**📝 PDF Creator Help**\n\n"
                "`/pdf` → Show help\n"
                "`/pdfdelete` → Delete all saved images\n"
                "`/pdfget <name>` → Generate PDF\n\n"
                "**How to use:**\n"
                "1️⃣ Reply to an image using `/pdf`\n"
                "2️⃣ Add more images by replying again\n"
                "3️⃣ Use `/pdfget name` to create PDF"
            )

        reply = await event.get_reply_message()
        if not reply.photo and not reply.document:
            return

        ensure_folder()

        file_path = await reply.download_media(file=os.path.join(PDF_TEMP, "img.jpg"))
        index = len(os.listdir(PDF_TEMP))
        new_path = os.path.join(PDF_TEMP, f"img_{index}.jpg")
        os.rename(file_path, new_path)

        await event.reply(f"✅ Image saved!\nTotal images: {index+1}")

    @bot.on(events.NewMessage(pattern=r"^/pdfdelete$"))
    async def pdf_delete(event):

        uid = event.sender_id
        mode = bot.mode.lower()
        if mode == "private":
            if uid != bot.owner_id and uid not in bot.sudo_users:
                return

        ensure_folder()
        for f in os.listdir(PDF_TEMP):
            os.remove(os.path.join(PDF_TEMP, f))
        await event.reply("🗑️ All saved images deleted!")

    @bot.on(events.NewMessage(pattern=r"^/pdfget (.+)"))
    async def pdf_get(event):

        uid = event.sender_id
        mode = bot.mode.lower()
        if mode == "private":
            if uid != bot.owner_id and uid not in bot.sudo_users:
                return

        name = event.pattern_match.group(1).strip()
        ensure_folder()
        files = sorted(os.listdir(PDF_TEMP))

        if not files:
            return await event.reply("❌ No images saved.")

        pdf_name = f"{name}.pdf"
        pdf_path = os.path.join(PDF_TEMP, pdf_name)
        image_paths = [os.path.join(PDF_TEMP, f) for f in files]

        try:
            with open(pdf_path, "wb") as pdf_file:
                pdf_file.write(img2pdf.convert(image_paths))

            await bot.send_file(event.chat_id, pdf_path, caption=f"📄 Your PDF: {pdf_name}")

        except Exception as e:
            return await event.reply(f"❌ Error: {e}")

        for f in image_paths:
            os.remove(f)
        os.remove(pdf_path)

        await event.reply("✅ PDF created and temporary files cleaned.")
