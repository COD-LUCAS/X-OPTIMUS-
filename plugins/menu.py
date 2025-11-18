import os
from telethon import events

MENU_IMAGE = "assets/menu.jpg"  # keep your menu.jpg here

# Core commands that are always available
CORE_COMMANDS = [
    {"cmd": "menu", "desc": "Show this command menu", "icon": "📋"},
    {"cmd": "alive", "desc": "Check if bot is running", "icon": "💚"},
    {"cmd": "checkupdate", "desc": "Check for updates", "icon": "🔍"},
    {"cmd": "update", "desc": "Update the bot", "icon": "⬆️"},
    {"cmd": "ping", "desc": "Check bot response time", "icon": "🏓"},
    {"cmd": "mode", "desc": "Change bot mode", "icon": "⚙️"},
    {"cmd": "install", "desc": "Install new plugins", "icon": "📥"}
]


def get_installed_plugins():
    """Get all installed plugins from plugins folder"""
    plugins = []
    plugins_dir = "plugins"
    
    # Core plugin files to exclude
    core_files = ["menu.py", "alive.py", "updater.py", "ping.py", "mode.py", "install.py", "__init__.py"]
    
    if os.path.exists(plugins_dir):
        for file in os.listdir(plugins_dir):
            if file.endswith(".py") and file not in core_files:
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
        
        # Build core commands section
        core_cmds = ""
        for cmd in CORE_COMMANDS:
            core_cmds += f"{cmd['icon']} `/{cmd['cmd']}` - {cmd['desc']}\n"
        
        # Build installed plugins section
        if installed_plugins:
            plugin_list = ""
            for i, plugin in enumerate(installed_plugins, 1):
                plugin_list += f"  {i}. `/{plugin}`\n"
            
            plugins_section = f"""
╭─────────────────────╮
│  📦 INSTALLED PLUGINS │
├─────────────────────┤
│ Total: {total_plugins} plugin(s)     │
╰─────────────────────╯

{plugin_list}
"""
        else:
            plugins_section = """
╭─────────────────────╮
│  📦 INSTALLED PLUGINS │
├─────────────────────┤
│ No plugins yet      │
│ Use /install to add │
╰─────────────────────╯
"""
        
        # Complete menu text
        text = f"""
╔═══════════════════════════╗
║   🤖 X-OPTIMUS BOT MENU   ║
╚═══════════════════════════╝

╭─────────────────────╮
│   ⚡ CORE COMMANDS   │
╰─────────────────────╯

{core_cmds}
{plugins_section}

╭─────────────────────╮
│      ℹ️ INFO         │
╰─────────────────────╯
📦 Version: Telethon 1.42.0
💡 Usage: /{'{command}'}
📖 Help: /help <command>

═══════════════════════════
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
