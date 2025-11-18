import time
import os
from telethon import events, Button

# Define the path for your ping asset
PING_ASSET_PATH = "assets/ping.jpg"
# You can use a URL for the GIF if you prefer not to store it locally
PING_GIF_URL = "https://i.imgur.com/GzG9l6n.gif" # Example fast-loading GIF

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/ping$"))
    async def ping_command(event):
        # 1. Start timer and react
        start_time = time.time()
        
        # React to the user's message
        await event.react("⚡️") 

        # 2. Send the GIF and asset
        try:
            # Check if the local asset exists, otherwise fall back to the GIF URL
            if os.path.exists(PING_ASSET_PATH):
                # Send the JPG file you mentioned
                message_sent = await event.reply(
                    f"Testing connection...",
                    file=PING_ASSET_PATH,
                    buttons=[Button.inline("Calculating...", data="ping_temp")]
                )
            else:
                # Send the GIF if the JPG is not found, or use a better GIF path
                message_sent = await event.reply(
                    f"Testing connection...",
                    file=PING_GIF_URL,
                    buttons=[Button.inline("Calculating...", data="ping_temp")]
                )

        except Exception as e:
            # Handle potential file/network errors during send
            await event.reply(f"❌ Failed to send asset: `{e}`")
            return

        # 3. Calculate and display results
        end_time = time.time()
        
        # Calculate the total time elapsed for the round-trip (start -> send -> end)
        ping_ms = round((end_time - start_time) * 1000) 
        
        # Create the response text
        response_text = f"**Pong!** 🏓\n"
        response_text += f"**Latency:** `{ping_ms} ms`\n"
        response_text += f"**Asset:** `assets/ping.jpg` {'✅ Found' if os.path.exists(PING_ASSET_PATH) else '⚠️ Not Found'}"
        
        # Edit the sent message to display the final result
        await message_sent.edit(response_text)

