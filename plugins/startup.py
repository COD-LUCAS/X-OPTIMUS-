import os
from telethon import events

sent = False  # avoid duplicate sends

def register(bot):

    @bot.on(events.ClientReady)
    async def startmsg(event):
        global sent
        if sent:
            return
        sent = True

        # YOUR ID
        owner = bot.me.id

        # Load sudo users from env (comma separated)
        sudo_raw = os.environ.get("SUDO_USERS", "")
        sudo_list = []

        if sudo_raw:
            for x in sudo_raw.split(","):
                try:
                    sudo_list.append(int(x.strip()))
                except:
                    continue

        # final list to send message
        targets = [owner] + sudo_list

        caption = (
            "🟢 **X-OPTIMUS Started Successfully!**\n"
            "Bot is now online and running. 🚀"
        )

        for user in targets:
            try:
                await bot.send_file(user, "assets/start.jpg", caption=caption)
            except:
                try:
                    await bot.send_message(user, caption)
                except:
                    pass
