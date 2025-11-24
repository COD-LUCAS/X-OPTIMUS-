import os
import requests
from telethon import events

MODELS = [
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash-thinking-exp",
    "gemini-exp-1206",
    "gemini-2.0-flash-lite",
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

    @bot.on(events.NewMessage(pattern=r"^/chatbot(?:\s+(.*))?$"))
    async def toggle(event):
        arg = event.pattern_match.group(1)
        api = os.getenv("GEMINI_API_KEY")

        if not arg:
            status = "✅ **ON**" if STATE.get(event.chat_id) else "❌ **OFF**"
            current_model = MODELS[MODEL.get(event.chat_id, 0)]
            msg_count = len(CONTEXT.get(event.chat_id, []))
            
            return await event.reply(
                f"**Chatbot Status:** {status}\n"
                f"**Model:** `{current_model}`\n"
                f"**Context:** {msg_count} messages\n\n"
                f"**Usage:**\n"
                f"`/chatbot on` - Enable\n"
                f"`/chatbot off` - Disable\n"
                f"`/chatbot clear` - Clear context\n"
                f"`/chatbot model` - Switch model"
            )

        if arg == "on":
            if not api:
                return await event.reply(HELP_TEXT)

            chat = event.chat_id
            STATE[chat] = True
            if chat not in CONTEXT:
                CONTEXT[chat] = []
            if chat not in MODEL:
                MODEL[chat] = 0
            
            return await event.reply(
                f"✅ **Chatbot Enabled**\n"
                f"🤖 Model: `{MODELS[0]}`\n\n"
                f"Just send me a message or reply to any message!"
            )

        if arg == "off":
            chat = event.chat_id
            STATE[chat] = False
            return await event.reply("❌ **Chatbot Disabled**")

        if arg == "clear":
            chat = event.chat_id
            CONTEXT[chat] = []
            MODEL[chat] = 0
            return await event.reply("🗑️ **Context cleared!**")

        if arg == "model":
            chat = event.chat_id
            idx = MODEL.get(chat, 0)
            idx = (idx + 1) % len(MODELS)
            MODEL[chat] = idx
            return await event.reply(f"🔄 **Switched to:** `{MODELS[idx]}`")

        return await event.reply(
            "❌ **Invalid command**\n\n"
            "Use:\n"
            "`/chatbot on` or `/chatbot off`"
        )

    # AUTO RESPONSE (DMs and Groups)
    @bot.on(events.NewMessage(incoming=True))
    async def auto_reply(event):
        # Skip outgoing messages
        if event.out:
            return

        chat = event.chat_id
        text = event.raw_text

        # Skip empty messages
        if not text or not text.strip():
            return

        # Skip if chatbot not enabled for this chat
        if not STATE.get(chat):
            return

        # Skip commands
        if text.startswith("/"):
            return

        # Skip if it's a media message without text
        if event.media and not text:
            return

        # Generate and send reply
        typing = await event.reply("💭 *Thinking...*")
        try:
            reply = await generate(event, text.strip())
            await typing.edit(reply)
        except Exception as e:
            await typing.edit(f"❌ Error: `{str(e)}`")

async def generate(event, msg):
    chat = event.chat_id
    api = os.getenv("GEMINI_API_KEY")

    if not api:
        return HELP_TEXT

    idx = MODEL.get(chat, 0)
    model = MODELS[idx]

    # Get last 10 messages from context
    history = CONTEXT.get(chat, [])[-10:]

    # Build payload
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": "You are a helpful AI assistant. Be concise and friendly."}]},
            *[
                {"role": h["role"], "parts": [{"text": h["text"]}]}
                for h in history
            ],
            {"role": "user", "parts": [{"text": msg}]}
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048,
        }
    }

    try:
        url = f"{API_URL}{model}:generateContent?key={api}"
        r = requests.post(url, json=payload, timeout=30)

        # Handle rate limiting
        if r.status_code == 429:
            if idx + 1 < len(MODELS):
                MODEL[chat] = idx + 1
                return await generate(event, msg)  # Retry with next model
            return "❌ **Rate limit reached on all models.** Please try again later."

        # Handle API errors
        if r.status_code != 200:
            error_msg = r.json().get("error", {}).get("message", "Unknown error")
            return f"❌ **API Error ({r.status_code}):**\n`{error_msg}`"

        data = r.json()
        
        # Extract reply
        try:
            reply = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )
        except (IndexError, KeyError):
            return "❌ **No response from API.** Try again."

        if not reply:
            return "❌ **Empty response.** The model may have blocked this request."

        # Save to context
        if chat not in CONTEXT:
            CONTEXT[chat] = []
        
        CONTEXT[chat].append({"role": "user", "text": msg})
        CONTEXT[chat].append({"role": "model", "text": reply})

        # Keep only last 20 exchanges (40 messages)
        if len(CONTEXT[chat]) > 40:
            CONTEXT[chat] = CONTEXT[chat][-40:]

        return reply

    except requests.Timeout:
        return "⏱️ **Request timeout.** Try again."
    except requests.RequestException as e:
        return f"❌ **Network Error:**\n`{str(e)}`"
    except Exception as e:
        return f"❌ **Error:**\n`{str(e)}`"
