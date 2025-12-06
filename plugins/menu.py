import os
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern="^/menu$"))
    async def menu(event):

        if bot.MODE == "PRIVATE" and event.sender_id != bot.owner_id:
            return

        # REAL MESSAGE REACTION ❤️
        try:
            await event.client.send_reaction(event.chat_id, event.id, "❤️")
        except:
            pass

        # Scan ONLY user plugins
        plugin_dir = "container_data/user_plugins"
        user_plugins = []
        if os.path.exists(plugin_dir):
            for f in os.listdir(plugin_dir):
                if f.endswith(".py"):
                    user_plugins.append("/" + f.replace(".py", ""))

        plugin_block = "\n".join(user_plugins) if user_plugins else "None"

        txt = f"""
❍⊷══〘 **X-OPTIMUS BOT** 〙══⊷❍

🕊️ **Available Commands**
━━━━━━━━━━━━━━━━━━━━━━
Use **/list** to get more info.
━━━━━━━━━━━━━━━━━━━━━━

**𝑩𝒂𝒔𝒊𝒄 𝑪𝒐𝒎𝒎𝒂𝒏𝒅𝒔**
━━━━━━━━━━
/ping
/alive
/info
/id
/uptime
/mode
/setvar
/delvar
/checkupdate
/update
/reboot
/list

**𝑩𝒖𝒊𝒍𝒕-𝒊𝒏 𝑭𝒆𝒂𝒕𝒖𝒓𝒆𝒔**
━━━━━━━━━━
/insta
/sticker 
/yt
/yta
/mp3
/img
/genimg
/rbg
/pdf
/url
/chatbot

**𝑼𝒔𝒆𝒓 𝑷𝒍𝒖𝒈𝒊𝒏𝒔**
━━━━━━━━━━
{plugin_block}
"""

        img = "assets/menu.jpg"
        if os.path.exists(img):
            await bot.send_file(event.chat_id, img, caption=txt)
        else:
            await event.reply(txt)
