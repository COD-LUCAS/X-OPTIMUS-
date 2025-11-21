import os
import img2pdf
from telethon import events
from PIL import Image

PDF_TEMP = "container_data/pdf_temp"

def ensure_folder():
    if not os.path.exists(PDF_TEMP):
        os.makedirs(PDF_TEMP)

def register(bot):
    
    @bot.on(events.NewMessage(pattern=r"^/pdf$"))
    async def pdf_help(event):
        await event.reply(
            "**📝 PDF Creator Help**\n\n"
            "`/pdf` → Show help\n"
            "`/pdfdelete` → Delete all saved images\n"
            "`/pdfget <name>` → Generate PDF with custom name\n\n"
            "**How to use:**\n"
            "1️⃣ Reply to any image using `/pdf`\n"
            "2️⃣ Add more images by replying again\n"
            "3️⃣ Finally use `/pdfget yourname`"
        )

    # -------------------------------------------
    # ADD IMAGE (reply to image)
    # -------------------------------------------
    @bot.on(events.NewMessage(pattern=r"^/pdf$"))
    async def add_image(event):
        if not event.is_reply:
            return
        
        reply = await event.get_reply_message()

        if not reply.photo and not reply.document:
            return
        
        ensure_folder()

        file_path = await reply.download_media(file=os.path.join(PDF_TEMP, "img.jpg"))

        # rename as numbered
        index = len(os.listdir(PDF_TEMP))
        new_path = os.path.join(PDF_TEMP, f"img_{index}.jpg")
        os.rename(file_path, new_path)

        await event.reply(
            f"✅ **Image saved!**\nTotal images: **{index+1}**\n"
            "Use `/pdfget filename` to generate the final PDF."
        )

    # -------------------------------------------
    # DELETE ALL
    # -------------------------------------------
    @bot.on(events.NewMessage(pattern=r"^/pdfdelete$"))
    async def pdf_delete(event):
        ensure_folder()
        for f in os.listdir(PDF_TEMP):
            os.remove(os.path.join(PDF_TEMP, f))
        await event.reply("🗑️ **All saved images deleted!**")

    # -------------------------------------------
    # GENERATE PDF
    # -------------------------------------------
    @bot.on(events.NewMessage(pattern=r"^/pdfget (.+)"))
    async def pdf_get(event):
        name = event.pattern_match.group(1).strip()
        
        ensure_folder()
        files = sorted(os.listdir(PDF_TEMP))

        if not files:
            return await event.reply("❌ No images saved! Use `/pdf` by replying to images.")

        pdf_name = f"{name}.pdf"
        pdf_path = os.path.join(PDF_TEMP, pdf_name)

        # convert images → PDF
        image_paths = [os.path.join(PDF_TEMP, f) for f in files]

        try:
            with open(pdf_path, "wb") as pdf_file:
                pdf_file.write(img2pdf.convert(image_paths))

            # send PDF
            await bot.send_file(event.chat_id, pdf_path, caption=f"📄 **Your PDF: {pdf_name}**")

        except Exception as e:
            return await event.reply(f"❌ PDF creation failed: {str(e)}")

        # cleanup
        for f in image_paths:
            os.remove(f)
        os.remove(pdf_path)

        await event.reply("✅ PDF successfully generated and cleaned temporary files!")
