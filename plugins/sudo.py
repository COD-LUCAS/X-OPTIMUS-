import os
from telethon import events

SUDO_FILE = "data/sudo.txt"

def get_sudo_list():
    if not os.path.exists(SUDO_FILE):
        return []
    with open(SUDO_FILE, "r") as f:
        return [x.strip() for x in f.readlines() if x.strip().isdigit()]

def save_sudo_list(ids):
    with open(SUDO_FILE, "w") as f:
        f.write("\n".join(ids))

def register(bot):

    @bot.on(events.NewMessage(pattern="/sudo add (\d+)"))
    async def add_sudo(event):
        owner = (await event.client.get_me()).id
        if event.sender_id != owner:
            return await event.reply("❌ Only the owner can manage sudo.")

        uid = event.pattern_match.group(1)
        sudo_list = get_sudo_list()

        if uid in sudo_list:
            return await event.reply("⚠️ This user is already a sudo member.")

        sudo_list.append(uid)
        save_sudo_list(sudo_list)
        await event.reply(f"✅ Added **{uid}** to sudo list.")

    @bot.on(events.NewMessage(pattern="/sudo remove (\d+)"))
    async def remove_sudo(event):
        owner = (await event.client.get_me()).id
        if event.sender_id != owner:
            return await event.reply("❌ Only the owner can manage sudo.")

        uid = event.pattern_match.group(1)
        sudo_list = get_sudo_list()

        if uid not in sudo_list:
            return await event.reply("⚠️ User is not a sudo member.")

        sudo_list.remove(uid)
        save_sudo_list(sudo_list)
        await event.reply(f"🗑 Removed **{uid}** from sudo list.")

    @bot.on(events.NewMessage(pattern="/sudo list"))
    async def list_sudo(event):
        sudo_list = get_sudo_list()
        if not sudo_list:
            return await event.reply("📜 No sudo members found.")

        txt = "🛡 **SUDO MEMBERS:**\n\n"
        txt += "\n".join([f"• `{x}`" for x in sudo_list])
        await event.reply(txt)
