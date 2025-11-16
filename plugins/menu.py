import os, json, requests
from telethon import events
from plugins.security import cfg

RAW_VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"

CORE_PLUGINS = [
    "menu",
    "ping",
    "alive",
    "install",
    "remove",
    "allplug",
    "update",
    "sudo"
]

def get_local_version():
    try:
        with open("version.json", "r", encoding="utf-8") as f:
            return json.load(f).get("version", "0.0.0")
    except:
        return "0.0.0"

def get_remote_version():
    try:
        return requests.get(RAW_VERSION_URL, timeout=5).json().get("version", "0.0.0")
    except:
        return "0.0.0"

def parse(v):
    try:
        return tuple(map(int, v.split(".")))
    except:
        return (0,)

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/menu$"))
    async def menu(event):

        local = get_local_version()
        remote = get_remote_version()

        if parse(remote) > parse(local):
            update_status = f"🆕 `{local}` → `{remote}` Update Available"
        elif parse(remote) == parse(local):
            update_status = f"✅ Up To Date `{local}`"
        else:
            update_status = f"⚠ Local Version Ahead `{local}`"

        files = os.listdir("plugins")
        installed = sorted([f[:-3] for f in files if f.endswith(".py")])

        core_list = "\n".join(f"• `{p}`" for p in CORE_PLUGINS if p in installed)
        user_list = "\n".join(f"• `{p}`" for p in installed if p not in CORE_PLUGINS)

        sudo_users = cfg["sudo"]
        sudo_list = "\n".join(f"• `{u}`" for u in sudo_users) if sudo_users else "• None"

        caption = (
            "**🟣 X-OPTIMUS CONTROL PANEL 🟣**\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🧩 **Version:** `{local}`\n"
            f"🔄 **Update:** {update_status}\n"
            f"🔐 **Mode:** `{cfg['mode']}`\n"
            f"👑 **Sudo Users:**\n{sudo_list}\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "🛠 **Core Plugins**\n"
            f"{core_list or '• None'}\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "🧩 **Installed Plugins**\n"
            f"{user_list or '• No extra plugins'}\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "📘 **Bot Commands**\n"
            "• `/menu` – Open control panel\n"
            "• `/ping` – Real ping report\n"
            "• `/alive` – Status card\n"
            "• `/mode` – Show mode\n"
            "• `/mode public/private` – Change mode\n"
            "• `/sudo add <id>` – Add SUDO\n"
            "• `/sudo del <id>` – Remove SUDO\n"
            "• `/sudo list` – List SUDO\n"
            "• `/install <url>` – Install plugin\n"
            "• `/remove <name>` – Delete plugin\n"
            "• `/allplug` – List plugins\n"
            "• `/update` – Update bot\n"
        )

        try:
            await bot.send_file(
                event.chat_id,
                "assets/menu.jpg",
                caption=caption,
                reply_to=event.id
            )
        except:
            await event.reply(caption)
