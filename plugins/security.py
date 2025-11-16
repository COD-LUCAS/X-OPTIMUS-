import json, os
from telethon import events

CONFIG_FILE = "security.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"mode": "public", "sudo": []}

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

cfg = load_config()

def is_sudo(user_id):
    return user_id in cfg["sudo"]

def is_allowed(event):
    uid = event.sender_id
    if uid is None:
        return False
    if uid == int(os.environ.get("OWNER", "0")):
        return True
    if is_sudo(uid):
        return True
    return cfg["mode"] == "public"

def register(bot):

    @bot.on(events.NewMessage(pattern="^/mode$"))
    async def mode_status(event):
        await event.reply(f"🔐 **Mode:** `{cfg['mode']}`")

    @bot.on(events.NewMessage(pattern="^/mode (.+)"))
    async def mode_set(event):
        uid = event.sender_id
        owner = int(os.environ.get("OWNER", "0"))
        if uid != owner:
            return

        mode = event.pattern_match.group(1).lower()
        if mode not in ["public", "private"]:
            return await event.reply("❌ Use: `/mode public` or `/mode private`")

        cfg["mode"] = mode
        save_config(cfg)
        await event.reply(f"🔐 Mode changed to **{mode}**")

    @bot.on(events.NewMessage(pattern="^/sudo add (\d+)"))
    async def sudo_add(event):
        uid = event.sender_id
        owner = int(os.environ.get("OWNER", "0"))
        if uid != owner:
            return

        user = int(event.pattern_match.group(1))
        if user not in cfg["sudo"]:
            cfg["sudo"].append(user)
            save_config(cfg)
        await event.reply(f"🟢 Added `{user}` to SUDO users.")

    @bot.on(events.NewMessage(pattern="^/sudo del (\d+)"))
    async def sudo_del(event):
        uid = event.sender_id
        owner = int(os.environ.get("OWNER", "0"))
        if uid != owner:
            return

        user = int(event.pattern_match.group(1))
        if user in cfg["sudo"]:
            cfg["sudo"].remove(user)
            save_config(cfg)
        await event.reply(f"🔴 Removed `{user}` from SUDO users.")

    @bot.on(events.NewMessage(pattern="^/sudo list$"))
    async def sudo_list(event):
        users = cfg["sudo"]
        if not users:
            return await event.reply("⚠ No SUDO users.")
        text = "🧑‍💻 **SUDO Users:**\n" + "\n".join(f"• `{u}`" for u in users)
        await event.reply(text)
