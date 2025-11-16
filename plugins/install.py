from telethon import events
import requests, importlib, os

def convert_to_raw(url):
    if "raw.githubusercontent.com" in url:
        return url

    if "github.com" in url and "/blob/" in url:
        return url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

    if url.startswith("https://github.com") and url.endswith(".py"):
        parts = url.split("github.com/")[1].split("/")
        user, repo = parts[0], parts[1]
        raw = url.replace("github.com", "raw.githubusercontent.com").replace(f"{repo}/blob", f"{repo}")
        return raw

    if "gist.github.com" in url:
        try:
            user = url.split("/")[3]
            gist_id = url.split("/")[-1]
            return f"https://gist.githubusercontent.com/{user}/{gist_id}/raw"
        except:
            return url

    return url

def register(bot):
    @bot.on(events.NewMessage(pattern=r"^/install (.+)"))
    async def _(event):
        url = event.pattern_match.group(1)
        url = convert_to_raw(url)

        name = url.split("/")[-1].split("?")[0].replace(".py", "")
        path = f"plugins/{name}.py"

        try:
            code = requests.get(url).text

            if "def register" not in code:
                return await event.reply("❌ Invalid plugin.")

            with open(path, "w", encoding="utf-8") as f:
                f.write(code)

            importlib.invalidate_caches()
            module = importlib.import_module(f"plugins.{name}")

            if hasattr(module, "register"):
                module.register(bot)

            await event.reply(f"✅ Installed `{name}.py`")

        except Exception as e:
            await event.reply(f"❌ {e}")
