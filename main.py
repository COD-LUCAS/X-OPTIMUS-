import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
STRING = os.environ.get("STRING_SESSION")

bot = TelegramClient(StringSession(STRING), API_ID, API_HASH)

@bot.on(events.NewMessage(pattern=r"\.alive"))
async def alive(event):
    await event.reply(
        "🤖 **X-OPTIMUS UserBot is Alive!**\n"
        "🔹 Powered by Telethon\n"
        "🔹 Developer: You\n"
    )

@bot.on(events.NewMessage(pattern=r"\.ping"))
async def ping(event):
    await event.reply("🏓 **PONG!**")

@bot.on(events.NewMessage(pattern=r"\.id"))
async def uid(event):
    await event.reply(f"🆔 Your ID: `{event.sender_id}`")

print("🚀 X-OPTIMUS USERBOT STARTED...")
bot.start()
bot.run_until_disconnected()
