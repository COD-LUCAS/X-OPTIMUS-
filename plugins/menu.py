import os
from telethon import events

MENU_IMAGE = "assets/menu.jpg"  # keep your menu.jpg here


def get_all_commands():
    """Automatically scan plugins folder and get all available commands"""
    commands = []
    plugins_dir = "plugins"
    
    if os.path.exists(plugins_dir):
        for file in os.listdir(plugins_dir):
            if file.endswith(".py") and file != "__init__.py":
                name = file[:-3]  # Remove .py extension
                commands.append(name)
    
    commands.sort()
    return commands


def register(bot):
    
    @bot.on(events.NewMessage(pattern=r"^/menu$"))
    async def menu(event):
        
        # Get all plugins automatically
        commands = get_all_commands()
        
        # Create command list with bullet points
        cmd_list = "\n".join([f"• {cmd}" for cmd in commands])
        
        # Count total plugins
        total = len(commands)
        
        text = f"""
🤖 **X-OPTIMUS COMMAND MENU**

📊 **Total Plugins:** {total}

━━━━━━━━━━━━━━━━━━━━
📋 **AVAILABLE COMMANDS:**
━━━━━━━━━━━━━━━━━━━━

{cmd_list}

━━━━━━━━━━━━━━━━━━━━
💡 **Usage:** /{'{command}'}
📦 **Version:** Telethon 1.42.0

Use /help <command> for details
"""
        
        if os.path.exists(MENU_IMAGE):
            await event.reply(
                file=MENU_IMAGE,
                message=text
            )
        else:
            await event.reply(text)
