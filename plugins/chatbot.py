import os
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from utils import edit_or_reply

CHATBOT_STATE = False
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key="

def is_admin(uid):
    return uid == Config.OWNER_ID or uid in Config.SUDO_USERS

@Client.on_message(filters.command("chatbot", prefixes=Config.HANDLER) & filters.me)
async def chatbot_handler(client, message: Message):
    global CHATBOT_STATE
    args = message.text.split()

    if len(args) < 2:
        return await edit_or_reply(
            message,
            "**Usage:**\n`/chatbot on`\n`/chatbot off`"
        )

    if not is_admin(message.from_user.id):
        return await edit_or_reply(message, "❌ Permission denied.")

    option = args[1].lower()

    if option == "on":
        api_key = Config.GEMINI_API_KEY
        if not api_key:
            return await edit_or_reply(
                message,
                "❌ **GEMINI_API_KEY Missing**\n\n"
                "Get API Key:\nhttps://aistudio.google.com/app/apikey\n\n"
                "Set it using:\n`/setvar GEMINI_API_KEY=your_api_key`"
            )
        CHATBOT_STATE = True
        return await edit_or_reply(message, "🤖 **Chatbot Enabled**")

    if option == "off":
        CHATBOT_STATE = False
        return await edit_or_reply(message, "⚠️ **Chatbot Disabled**")
