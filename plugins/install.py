@dp.message_handler(commands=['install'])
async def install_plugin(message: types.Message):
    import aiohttp, os
    
    # Split command
    parts = message.text.split(" ")
    if len(parts) < 2:
        return await message.reply("❌ Usage: /install <raw_plugin_url>")

    url = parts[1]

    # Basic validation
    if not url.startswith("http"):
        return await message.reply("❌ Invalid URL")

    await message.reply("⏳ Downloading plugin...")

    try:
        # Try downloading
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await message.reply(f"❌ Error downloading plugin (HTTP {resp.status})")

                plugin_code = await resp.text()

        # Save plugin
        plugin_name = url.split("/")[-1]
        folder = "plugins"

        # Create folder if not exist
        if not os.path.exists(folder):
            os.makedirs(folder)

        path = f"{folder}/{plugin_name}"

        with open(path, "w", encoding="utf-8") as f:
            f.write(plugin_code)

        await message.reply(
            f"✅ Plugin Installed Successfully!\n"
            f"📄 File: `{plugin_name}`\n"
            f"📁 Saved to: `{path}`\n"
            f"⚠️ Restart bot to load plugin."
        )

    except Exception as e:
        await message.reply(f"❌ Error: `{str(e)}`")
