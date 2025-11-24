import os
import requests
from telethon import events

MODELS = [
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash",
    "gemma-3-12b-it"
]

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/"

STATE = {}
CONTEXT = {}
MODEL = {}

HELP_TEXT = """❌ GEMINI_API_KEY Not Set

Get your API key:
https://aistudio.google.com/app/apikey

Then set it:
`/setvar GEMINI_API_KEY=YOUR_KEY`

After that, enable chatbot:
`/chatbot on`
"""

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/chatbot(?:\s+(.*))?$"))
    async def toggle(event):
        arg = event.pattern_match.group(1)
        api = os.getenv("GEMINI_API_KEY")

        if not arg:
            return await event.reply("Usage:\n/chatbot on\n/chatbot off")

        if arg == "on":
            if not api:
                return await event.reply(HELP_TEXT)

            chat = event.chat_id
            STATE[chat] = True
            CONTEXT[chat] = []
            MODEL[chat] = 0
            return await event.reply("✅ Chatbot Enabled")

        if arg == "off":
            chat = event.chat_id
            STATE[chat] = False
            CONTEXT.pop(chat, None)
            return await event.reply("❌ Chatbot Disabled")

        return await event.reply("❌ Invalid\nUse /chatbot on or /chatbot off")

    # DM AUTO RESPONSE
    @bot.on(events.NewMessage())
    async def dm_reply(event):
        if event.out:
            return

        chat = event.chat_id
        text = event.raw_text.strip()

        if not text:
            return

        if not STATE.get(chat):
            return

        if text.startswith("/"):
            return

        reply = await generate(event, text)
        await event.reply(reply)

async def generate(event, msg):
    chat = event.chat_id
    api = os.getenv("GEMINI_API_KEY")

    if not api:
        return HELP_TEXT

    idx = MODEL.get(chat, 0)
    model = MODELS[idx]

    history = CONTEXT.get(chat, [])[-10:]

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": "System: You are a helpful assistant."}]},
            *[
                {"role": h["role"], "parts": [{"text": h["text"]}]}
                for h in history
            ],
            {"role": "user", "parts": [{"text": msg}]}
        ]
    }

    try:
        url = f"{API_URL}{model}:generateContent?key={api}"
        r = requests.post(url, json=payload, timeout=20)

        if r.status_code == 429:
            if idx + 1 < len(MODELS):
                MODEL[chat] = idx + 1
                return "⚠️ Rate limit. Trying another model..."
            return "❌ All models limited. Try later."

        data = r.json()
        reply = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "❌ No response.")
        )

        if chat not in CONTEXT:
            CONTEXT[chat] = []
        CONTEXT[chat].append({"role": "user", "text": msg})
        CONTEXT[chat].append({"role": "model", "text": reply})

        return reply

    except Exception as e:
        return f"❌ API Error:\n`{str(e)}`"
