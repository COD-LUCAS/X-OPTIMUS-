import os
import requests
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/(genimg|aiimg)(?:\s+(.*))?$"))
    async def ai_generate(event):
        cmd = event.pattern_match.group(1)
        prompt = event.pattern_match.group(2)

        # HELP MESSAGE
        if not prompt:
            return await event.reply(
                "🎨 **AI IMAGE GENERATOR**\n\n"
                "**Usage:**\n"
                "`/gen your prompt`\n"
                "Example: `/gen cyberpunk robot cat`\n\n"
                "🧩 **API Required (OpenAI)**\n"
                "Follow these steps:\n"
                "1️⃣ Go to https://platform.openai.com/\n"
                "2️⃣ Login → Click **API Keys**\n"
                "3️⃣ Create new key\n"
                "4️⃣ Copy the key\n"
                "5️⃣ Set it inside bot using:\n"
                "```\n"
                "/setvar IMG_API_KEY=your_openai_key_here\n"
                "```\n\n"
                "✔ Supported Models: DALL·E, GPT-Image-1\n"
            )

        api_key = os.getenv("IMG_API_KEY")

        if not api_key:
            return await event.reply(
                "❌ **IMG_API_KEY missing!**\n\n"
                "Get OpenAI key from:\n"
                "👉 https://platform.openai.com/api-keys\n\n"
                "Then set it using:\n"
                "`/setvar IMG_API_KEY=your_key_here`"
            )

        processing = await event.reply(f"🎨 Generating image for: **{prompt}** ...")

        # ---- OPENAI IMAGE GENERATION ----
        try:
            url = "https://api.openai.com/v1/images/generations"

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

            body = {
                "model": "gpt-image-1",
                "prompt": prompt,
                "size": "1024x1024"
            }

            response = requests.post(url, headers=headers, json=body, timeout=60)

            if response.status_code != 200:
                return await processing.edit(f"❌ API Error:\n`{response.text}`")

            data = response.json()
            img_url = data["data"][0]["url"]

            await bot.send_file(
                event.chat_id,
                img_url,
                caption=f"✨ **AI Image Generated**\n📝 Prompt: `{prompt}`\n\nModel: GPT-Image-1"
            )

            await processing.delete()

        except Exception as e:
            await processing.edit(f"❌ Unexpected Error:\n`{e}`")
