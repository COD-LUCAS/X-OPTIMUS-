import os
from telethon import events

def register(bot):

    @bot.on(events.NewMessage(pattern="^/list$"))
    async def list_commands(event):
        # PRIVATE mode check
        if bot.MODE == "PRIVATE" and event.sender_id != bot.owner_id:
            return

        # Quick reaction
        try:
            await event.react("📋")
        except:
            pass

        # All commands with descriptions
        commands = {
            "**⚙️ BASIC COMMANDS**": {
                "/ping": "Check bot response speed",
                "/alive": "Check if bot is running",
                "/info": "Show bot information",
                "/id": "Get your user/chat ID",
                "/uptime": "Show bot uptime"
            },
            "**🔧 ADMIN COMMANDS**": {
                "/mode": "Switch public/private mode",
                "/setvar": "Set environment variable",
                "/delvar": "Delete environment variable",
                "/checkupdate": "Check for bot updates",
                "/update": "Update bot to latest version",
                "/reboot": "Restart the bot"
            },
            "**📥 DOWNLOADERS**": {
                "insta <url>": "Download Instagram media",
                "yt <url>": "Download YouTube video",
                "yta <url>": "Download YouTube audio",
                "img <url>": "Download image from URL"
            },
            "**🎨 MEDIA TOOLS**": {
                "mp3": "Convert video to MP3 (reply to video)",
                "genimg <prompt>": "Generate AI image",
                "rbg": "Remove background (reply to image)",
                "pdf": "Convert images to PDF (reply to images)",
                "url": "Upload to Catbox (reply to media)"
            },
            "**🤖 AI FEATURES**": {
                "chatbot": "Toggle auto-reply chatbot"
            }
        }

        # Build response
        txt = "**📋 ALL COMMANDS**\n\n"
        
        for category, cmds in commands.items():
            txt += f"{category}\n"
            for cmd, desc in cmds.items():
                txt += f"`{cmd}` - {desc}\n"
            txt += "\n"

        # Scan user plugins
        user_plugins = []
        plugin_dir = "container_data/user_plugins"
        if os.path.exists(plugin_dir):
            user_plugins = [
                f[:-3] for f in os.listdir(plugin_dir) 
                if f.endswith(".py") and not f.startswith("_")
            ]

        if user_plugins:
            txt += f"**🔌 CUSTOM PLUGINS ({len(user_plugins)})**\n"
            for plugin in user_plugins:
                txt += f"`{plugin}` - Custom plugin\n"
            txt += "\n"

        txt += "💡 Type `/menu` for quick view"

        await event.reply(txt, link_preview=False)
