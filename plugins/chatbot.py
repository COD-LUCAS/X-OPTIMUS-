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
            status = "✅ ON" if STATE.get(chat) else "❌ OFF"
            model = MODELS[MODEL.get(chat, 0)]
            msgs = len(CONTEXT.get(chat, []))
            api_status = "✅ Set" if api else "❌ Not Set"
            
            return await event.edit(
                f"**🤖 Chatbot Debug Info**\n\n"
                f"Status: {status}\n"
                f"API Key: {api_status}\n"
                f"Model: `{model}`\n"
                f"Context: {msgs} messages\n"
                f"Chat ID: `{chat}`\n\n"
                f"**Commands:**\n"
                f"`/chatbot on` - Enable\n"
                f"`/chatbot off` - Disable\n"
                f"`/chatbot test` - Test response\n"
                f"`/chatbot clear` - Clear history"
            )

        if arg == "on":
            if not api:
                return await event.edit(HELP_TEXT)

            STATE[chat] = True
            CONTEXT[chat] = []
            MODEL[chat] = 0
            
            await event.edit(
                f"✅ **Chatbot Enabled**\n"
                f"Model: `{MODELS[0]}`\n"
                f"Chat: `{chat}`\n\n"
                f"✨ Now send any message!"
            )

        elif arg == "off":
            STATE[chat] = False
            await event.edit("❌ **Chatbot Disabled**")

        elif arg == "clear":
            CONTEXT[chat] = []
            MODEL[chat] = 0
            await event.edit("🗑️ **History cleared**")

        elif arg == "test":
            if not STATE.get(chat):
                return await event.edit("⚠️ Enable chatbot first: `/chatbot on`")
            
            msg = await event.reply("🧪 Testing API...")
            reply = await generate(chat, "Say 'Hi! I'm working!' in a friendly way")
            await msg.edit(f"**Test Result:**\n\n{reply}")

        else:
            await event.edit("❌ Invalid. Use: `/chatbot on` or `/chatbot off`")

    # This is the main message handler
    @bot.on(events.NewMessage(incoming=True))
    async def auto_reply(event):
        # Debug: Log every incoming message
        print(f"[DEBUG] Message from {event.chat_id}: {event.text}")
        
        chat = event.chat_id
        text = event.text
        
        # Skip if no text
        if not text:
            print(f"[DEBUG] Skipped - no text")
            return
        
        # Skip commands
        if text.startswith('/'):
            print(f"[DEBUG] Skipped - is command")
            return
        
        # Check if enabled
        if not STATE.get(chat):
            print(f"[DEBUG] Skipped - chatbot disabled for {chat}")
            print(f"[DEBUG] Current STATE: {STATE}")
            return
        
        print(f"[DEBUG] Processing message: {text}")
        
        # Generate reply
        try:
            async with bot.action(chat, 'typing'):
                reply = await generate(chat, text.strip())
            
            await event.reply(reply)
            print(f"[DEBUG] Replied successfully")
        except Exception as e:
            print(f"[DEBUG] Error: {e}")
            await event.reply(f"❌ Error: {str(e)}")

async def generate(chat, msg):
    api = os.getenv("GEMINI_API_KEY")

    if not api:
        return "❌ API key not set"

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
        }
    }

    try:
        url = f"{API_URL}{model}:generateContent?key={api}"
        r = requests.post(url, json=payload, timeout=30)

        if r.status_code == 429:
            if idx + 1 < len(MODELS):
                MODEL[chat] = idx + 1
                return await generate(chat, msg)
            return "⚠️ Rate limit. Try later."

        if r.status_code != 200:
            return f"❌ API Error {r.status_code}"

        data = r.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"]

        # Save context
        if chat not in CONTEXT:
            CONTEXT[chat] = []
        
        CONTEXT[chat].append({"role": "user", "text": msg})
        CONTEXT[chat].append({"role": "model", "text": reply})

        if len(CONTEXT[chat]) > 20:
            CONTEXT[chat] = CONTEXT[chat][-20:]

        return reply

    except Exception as e:
        return f"❌ Error: {str(e)}"
