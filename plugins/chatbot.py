import os
import requests
from telethon import events

MODELS = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b"
]

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/"

STATE = {}
CONTEXT = {}
MODEL = {}

HELP_TEXT = """❌ GEMINI_API_KEY Not Set

Get API key:
https://aistudio.google.com/app/apikey

Set it:
`/setvar GEMINI_API_KEY=YOUR_KEY`

Then enable chatbot:
`/chatbot on`
"""

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/chatbot(?:\s+(.*))?$"))
    async def toggle(event):
        owner = os.getenv("OWNER", "")
        if str(event.sender_id) != owner:
            return await event.reply("🦉 Only owner can use this command")

        arg = event.pattern_match.group(1)
        api = os.getenv("GEMINI_API_KEY")
        chat = event.chat_id

        if not arg:
            status = "ON" if STATE.get(chat) else "OFF"
            api_status = "Set" if api else "Not Set"
            model = MODELS[MODEL.get(chat, 0)]
            msgs = len(CONTEXT.get(chat, []))

            return await event.reply(
                f"🤖 **Chatbot Status**\n\n"
                f"Status: `{status}`\n"
                f"API Key: `{api_status}`\n"
                f"Model: `{model}`\n"
                f"Context: `{msgs}` msgs\n\n"
                f"Commands:\n"
                f"/chatbot on\n"
                f"/chatbot off\n"
                f"/chatbot clear\n"
                f"/chatbot test"
            )

        if arg == "on":
            if not api:
                return await event.reply(HELP_TEXT)

            STATE[chat] = True
            CONTEXT[chat] = []
            MODEL[chat] = 0
            return await event.reply("✅ Chatbot Enabled")

        if arg == "off":
            STATE[chat] = False
            return await event.reply("❌ Chatbot Disabled")

        if arg == "clear":
            CONTEXT[chat] = []
            MODEL[chat] = 0
            return await event.reply("🗑️ Chat history cleared")

        if arg == "test":
            if not STATE.get(chat):
                return await event.reply("Enable first: /chatbot on")
            reply = await generate(chat, "Say 'Chatbot working!'")
            return await event.reply(f"Test Result:\n\n{reply}")

        return await event.reply("Invalid command")

    @bot.on(events.NewMessage(incoming=True))
    async def auto(event):
        text = event.raw_text
        chat = event.chat_id

        if not text or text.startswith("/"):
            return
        
        if not STATE.get(chat):
            return

        try:
            async with bot.action(chat, 'typing'):
                reply = await generate(chat, text)
            await event.reply(reply)
        except:
            pass


async def generate(chat, msg):
    api = os.getenv("GEMINI_API_KEY")
    if not api:
        return "API key missing"

    idx = MODEL.get(chat, 0)
    model = MODELS[idx]
    history = CONTEXT.get(chat, [])[-10:]

    payload = {
        "contents": [
            *[
                {
                    "role": h["role"],
                    "parts": [{"text": h["text"]}]
                }
                for h in history
            ],
            {"role": "user", "parts": [{"text": msg}]}
        ],
        "generationConfig": {"temperature": 0.8}
    }

    try:
        r = requests.post(
            f"{API_URL}{model}:generateContent?key={api}",
            json=payload,
            timeout=20
        )

        if r.status_code == 429:
            if idx + 1 < len(MODELS):
                MODEL[chat] = idx + 1
                return await generate(chat, msg)
            return "Rate limit hit"

        if r.status_code != 200:
            return f"API Error {r.status_code}"

        data = r.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"]

        if chat not in CONTEXT:
            CONTEXT[chat] = []

        CONTEXT[chat].append({"role": "user", "text": msg})
        CONTEXT[chat].append({"role": "model", "text": reply})

        if len(CONTEXT[chat]) > 20:
            CONTEXT[chat] = CONTEXT[chat][-20:]

        return reply

    except Exception as e:
        return f"Error: {str(e)}"
