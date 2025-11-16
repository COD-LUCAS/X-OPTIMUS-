@bot.on(events.NewMessage(pattern=r"^/install (.+)"))
async def install_plugin(event):
    url = event.pattern_match.group(1)

    if not url.startswith("http"):
        return await event.reply("❌ Invalid link.")

    # auto-detect plugin name
    name = url.split("/")[-1].split("?")[0].replace(".py", "")
    path = f"plugins/{name}.py"

    if os.path.exists(path):
        return await event.reply("⚠ Plugin already installed.")

    try:
        code = requests.get(url).text

        if not code or "def register" not in code:
            return await event.reply("❌ Not a valid plugin file.")

        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        importlib.invalidate_caches()
        module = importlib.import_module(f"plugins.{name}")
        plugins[name] = module

        if hasattr(module, "register"):
            module.register(bot)

        await event.reply(f"✅ Installed plugin `{name}.py`")

    except Exception as e:
        await event.reply(f"❌ Error: {e}")
