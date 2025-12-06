import os
import requests
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/(genimg|aiimg)(?:\s+(.*))?$"))
    async def ai_generate(event):

        mode = bot.mode.lower()
        uid = event.sender_id

        # PRIVATE MODE → ONLY OWNER + SUDO
        if mode == "private":
            if uid != bot.owner_id and uid not in bot.sudo_users:
                return await event.reply("❌ Private mode: only owner or sudo can generate AI images.")

        prompt = event.pattern_match.group(2)

        # HELP
        if not prompt:
            return await event.reply(
                "🎨 **AI IMAGE GENERATOR**\n\n"
                "**Usage:** `/genimg your prompt`\n"
                "Example: `/genimg cyberpunk robot cat`\n\n"
                "🧩 **API Required (OpenAI GPT-Image-1)**\n"
                "Get key: https://platform.openai.com/api-keys\n\n"
                "Set key:\n"
                "`/setvar IMG_API_KEY=your_openai_key_here`"
            )

        api_key = os.getenv("IMG_API_KEY")
        if not api_key:
            return await event.reply(
                "❌ **IMG_API_KEY missing!**\n\n"
                "Get your OpenAI API key here:\n"
                "👉 https://platform.openai.com/api-keys\n\n"
                "Set using:\n"
                "`/setvar IMG_API_KEY=your_key_here`"
            )

        status = await event.reply(f"🎨 Generating image for: **{prompt}** ...")

        # ---- NEW OPENAI IMAGE API (WORKING) ----
        try:
            url = "https://api.openai.com/v1/images/generations"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": "gpt-image-1",
                "prompt": prompt,
                "size": "1024x1024"
            }

            res = requests.post(url, headers=headers, json=payload, timeout=60)

            if res.status_code != 200:
                return await status.edit(f"❌ API Error:\n`{res.text}`")

            data = res.json()
            img_url = data["data"][0]["url"]

            await bot.send_file(
                event.chat_id,
                img_url,
                caption=f"✨ **AI Image Generated**\n📝 Prompt: `{prompt}`\nModel: GPT-Image-1"
            )

            await status.delete()

        except Exception as e:
            await status.edit(f"❌ Unexpected Error:\n`{e}`")
