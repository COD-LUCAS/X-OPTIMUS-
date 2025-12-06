import os
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern="^/menu$"))
    async def menu(event):

        uid = event.sender_id
        mode = bot.mode.lower()

        if mode == "private":
            if uid != bot.owner_id and uid not in bot.sudo_users:
                return

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

**𝑨𝒅𝒎𝒊𝒏 𝑪𝒐𝒎𝒎𝒂𝒏𝒅𝒔**
━━━━━━━━━━
/mode
/setvar
/delvar
/setsudo
/delsudo
/plugins
/install
/remove
/checkupdate
/update
/reboot
/list

**𝑩𝒖𝒊𝒍𝒕-𝒊𝒏 𝑭𝒆𝒂𝒕𝒖𝒓𝒆𝒔**
━━━━━━━━━━
/insta
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
