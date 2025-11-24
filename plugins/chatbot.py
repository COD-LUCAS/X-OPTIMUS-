import os
import requests
from telethon import events

MODELS = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-pro"
]

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/"

STATE = {}
CONTEXT = {}
MODEL = {}
PROMPT = {}

HELP_TEXT = """❌ GEMINI_API_KEY Not Found

Get free API key:
https://aistudio.google.com/app/apikey

Set it:
`/setvar GEMINI_API_KEY=YOUR_KEY`

Then enable chatbot:
`/chatbot on`
"""

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/chatbot(?:\s+(.*))?$", outgoing=True))
    async def manage(event):
        arg = (event.pattern_match.group(1) or "").strip()
        chat = event.chat_id
        api = os.getenv("GEMINI_API_KEY")

        if not arg:
            s = "ON ✅" if STATE.get(chat) else "OFF ❌"
            key = "SET ✅" if api else "NOT SET ❌"
            model = MODELS[MODEL.get(chat, 0)]
            ctx = len(CONTEXT.get(chat, []))
            return await event.edit(
                f"🤖 **Chatbot Status**\n\n"
                f"Status: **{s}**\n"
                f"API Key: **{key}**\n"
                f"Model: `{model}`\n"
                f"Context: `{ctx}` messages\n\n"
                f"Commands:\n"
                f"`/chatbot on`\n"
                f"`/chatbot off`\n"
                f"`/chatbot clear`\n"
                f"`/chatbot test`\n"
                f"`/chatbot setprompt <text>`"
            )

        if arg == "on":
            if not api:
                return await event.edit(HELP_TEXT)
            STATE[chat] = True
            CONTEXT[chat] = []
            MODEL[chat] = 0
            PROMPT[chat] = "You are a helpful assistant."
            return await event.edit("✅ Chatbot Enabled")

        if arg == "off":
            STATE[chat] = False
            return await event.edit("❌ Chatbot Disabled")

        if arg == "clear":
            CONTEXT[chat] = []
            MODEL[chat] = 0
            return await event.edit("🗑️ Chat history cleared")

        if arg.startswith("setprompt"):
            text = arg.replace("setprompt", "").strip()
            if not text:
                return await event.edit("❌ Usage: `/chatbot setprompt your text`")
            PROMPT[chat] = text
            return await event.edit("✅ Prompt updated")

        if arg == "test":
            if not api:
                return await event.edit(HELP_TEXT)
            if not STATE.get(chat):
                return await event.edit("❌ Enable chatbot first: `/chatbot on`")
            msg = await event.reply("🧪 Testing…")
            reply = await generate(chat, "Say 'Chatbot working!'")
            return await msg.edit(f"**Test Result:**\n\n{reply}")

        return await event.edit("❌ Invalid argument")

    @bot.on(events.NewMessage(incoming=True))
    async def auto(event):
        chat = event.chat_id
        text = event.text or ""

        if not STATE.get(chat):
            return

        if not text:
            return

        if text.startswith("/"):
            return

        try:
            async with bot.action(chat, "typing"):
                reply = await generate(chat, text.strip())
            await event.reply(reply)
        except Exception as e:
            await event.reply(f"❌ AI Error: {str(e)}")

async def generate(chat, message):
    api = os.getenv("GEMINI_API_KEY")
    if not api:
        return "❌ API key missing"

    idx = MODEL.get(chat, 0)
    model = MODELS[idx]

    history = CONTEXT.get(chat, [])[ -10 : ]
    system_prompt = PROMPT.get(chat, "You are a helpful assistant.")

    payload = {
        "contents": [
            {"role": "system", "parts": [{"text": system_prompt}]},
            *[
                {"role": h["role"], "parts": [{"text": h["text"]}]}
                for h in history
            ],
            {"role": "user", "parts": [{"text": message}]}
        ]
    }

    try:
        url = f"{API_URL}{model}:generateContent?key={api}"
        r = requests.post(url, json=payload, timeout=30)

        if r.status_code == 429:
            if idx + 1 < len(MODELS):
                MODEL[chat] = idx + 1
                return await generate(chat, message)
            return "⚠️ Rate limit reached. Try later."

        if r.status_code != 200:
            return f"❌ API Error {r.status_code}"

        data = r.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"]

        if chat not in CONTEXT:
            CONTEXT[chat] = []

        CONTEXT[chat].append({"role": "user", "text": message})
        CONTEXT[chat].append({"role": "model", "text": reply})

        if len(CONTEXT[chat]) > 20:
            CONTEXT[chat] = CONTEXT[chat][-20:]

        return reply

    except Exception as e:
        return f"❌ Error: {str(e)}"
