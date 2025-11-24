import os
import requests
from telethon import events

MODELS = [
    "gemini-2.0-flash-exp",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
]

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/"

STATE = {}
CONTEXT = {}
MODEL = {}

HELP_TEXT = """❌ **GEMINI_API_KEY Not Set**

Get your API key:
https://aistudio.google.com/app/apikey

Then set it:
`/setvar GEMINI_API_KEY=YOUR_KEY`

After that, enable chatbot:
`/chatbot on`
"""

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/chatbot(?:\s+(.*))?$", outgoing=True))
    async def toggle(event):
        arg = event.pattern_match.group(1)
        api = os.getenv("GEMINI_API_KEY")
        chat = event.chat_id

        if not arg:
            status = "✅ Enabled" if STATE.get(chat) else "❌ Disabled"
            model = MODELS[MODEL.get(chat, 0)]
            msgs = len(CONTEXT.get(chat, []))
            
            return await event.edit(
                f"**Chatbot Status**\n\n"
                f"Status: {status}\n"
                f"Model: `{model}`\n"
                f"Messages: {msgs}\n\n"
                f"**Commands:**\n"
                f"`/chatbot on` - Enable\n"
                f"`/chatbot off` - Disable\n"
                f"`/chatbot clear` - Clear history\n"
                f"`/chatbot model` - Switch model"
            )

        if arg == "on":
            if not api:
                return await event.edit(HELP_TEXT)

            STATE[chat] = True
            CONTEXT[chat] = []
            MODEL[chat] = 0
            
            return await event.edit(
                f"✅ **Chatbot Enabled**\n"
                f"Model: `{MODELS[0]}`\n\n"
                f"Send any message and I'll reply!"
            )

        elif arg == "off":
            STATE[chat] = False
            return await event.edit("❌ **Chatbot Disabled**")

        elif arg == "clear":
            CONTEXT[chat] = []
            MODEL[chat] = 0
            return await event.edit("🗑️ **History cleared**")

        elif arg == "model":
            idx = MODEL.get(chat, 0)
            idx = (idx + 1) % len(MODELS)
            MODEL[chat] = idx
            return await event.edit(f"🔄 **Model:** `{MODELS[idx]}`")

        else:
            return await event.edit("❌ Use: `/chatbot on` or `/chatbot off`")

    @bot.on(events.NewMessage(incoming=True, func=lambda e: not e.text.startswith('/')))
    async def auto_reply(event):
        chat = event.chat_id
        
        # Check if chatbot is enabled for this chat
        if not STATE.get(chat):
            return
        
        text = event.text
        if not text or not text.strip():
            return

        # Show typing indicator
        async with bot.action(chat, 'typing'):
            reply = await generate(chat, text.strip())
        
        await event.reply(reply)

async def generate(chat, msg):
    api = os.getenv("GEMINI_API_KEY")

    if not api:
        return "❌ API key not set. Use `/chatbot` for setup help."

    idx = MODEL.get(chat, 0)
    model = MODELS[idx]
    history = CONTEXT.get(chat, [])[-10:]

    payload = {
        "contents": [
            *[{"role": h["role"], "parts": [{"text": h["text"]}]} for h in history],
            {"role": "user", "parts": [{"text": msg}]}
        ],
        "generationConfig": {
            "temperature": 0.9,
            "maxOutputTokens": 2048,
        },
        "systemInstruction": {
            "parts": [{"text": "You are a helpful AI assistant. Be concise, friendly and natural."}]
        }
    }

    try:
        url = f"{API_URL}{model}:generateContent?key={api}"
        r = requests.post(url, json=payload, timeout=30)

        if r.status_code == 429:
            if idx + 1 < len(MODELS):
                MODEL[chat] = idx + 1
                return await generate(chat, msg)
            return "⚠️ Rate limit reached. Try again in a few minutes."

        if r.status_code == 400:
            error = r.json().get("error", {})
            msg_text = error.get("message", "Unknown error")
            return f"❌ API Error: {msg_text}"

        if r.status_code != 200:
            return f"❌ Error {r.status_code}: {r.text[:200]}"

        data = r.json()
        
        try:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "❌ Invalid API response. Try again."

        if not reply:
            return "❌ Empty response from AI."

        # Save context
        if chat not in CONTEXT:
            CONTEXT[chat] = []
        
        CONTEXT[chat].append({"role": "user", "text": msg})
        CONTEXT[chat].append({"role": "model", "text": reply})

        # Keep last 20 messages
        if len(CONTEXT[chat]) > 20:
            CONTEXT[chat] = CONTEXT[chat][-20:]

        return reply

    except requests.Timeout:
        return "⏱️ Timeout. Try again."
    except Exception as e:
        return f"❌ Error: {str(e)[:200]}"
