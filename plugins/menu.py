import os
from telethon import events

MENU_IMAGE = "assets/menu.jpg"  # keep your menu.jpg here

# Core commands that are always available
CORE_COMMANDS = [
    "menu",
    "alive", 
    "checkupdate",
    "update",
    "ping",
    "mode",
    "install",
    "reboot"
]


def get_installed_plugins():
    """Get all installed plugins from plugins folder"""
    plugins = []
    plugins_dir = "plugins"
    
    # Files to exclude from plugin list
    exclude_files = [
        "menu.py", "alive.py", "updater.py", "ping.py", 
        "mode.py", "install.py", "__init__.py",
        "auto_update_notify.py", "startup.py", "reboot.py",
        "sudo.py", "checkupdate.py", "update.py"
    ]
    
    if os.path.exists(plugins_dir):
        for file in os.listdir(plugins_dir):
            if file.endswith(".py") and file not in exclude_files:
                name = file[:-3]  # Remove .py extension
                plugins.append(name)
    
    plugins.sort()
    return plugins


def register(bot):
    
    @bot.on(events.NewMessage(pattern=r"^/menu$"))
    async def menu(event):
        
        # Get installed plugins
        installed_plugins = get_installed_plugins()
        total_plugins = len(installed_plugins)
        
        # Build core commands list
        core_list = "\n".join([f"• {cmd}" for cmd in CORE_COMMANDS])
        
        # Build installed plugins list
        if installed_plugins:
            plugin_list = "\n".join([f"• {plugin}" for plugin in installed_plugins])
            plugins_section = f"""
📦 **INSTALLED PLUGINS:**
━━━━━━━━━━━━━━━━━━━━

{plugin_list}
"""
        else:
            plugins_section = ""
        
        # Complete menu text
        text = f"""
🤖 **X-OPTIMUS COMMAND MENU**

📊 **Total Plugins:** {total_plugins}

━━━━━━━━━━━━━━━━━━━━
⚡ **CORE COMMANDS:**
━━━━━━━━━━━━━━━━━━━━

{core_list}
{plugins_section}
━━━━━━━━━━━━━━━━━━━━
💡 **Usage:** /{'{command}'}
📦 **Version:** Telethon 1.42.0

Use /help <command> for details
"""
        
        # Add reaction to user's message
        try:
            await event.react("📋")
        except:
            pass  # Ignore if reaction fails
        
        # Send with image if available
        if os.path.exists(MENU_IMAGE):
            await event.reply(
                file=MENU_IMAGE,
                message=text
            )
        else:
            await event.reply(text)
