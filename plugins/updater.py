from telethon import events
import os
import sys
import json
import requests

RAW_VERSION_URL = "https://raw.githubusercontent.com/COD-LUCAS/X-OPTIMUS/main/version.json"


def parse_version(v: str):
    try:
        return tuple(map(int, v.split(".")))
    except Exception:
        return (0, 0, 0)


def get_versions():
    with open("version.json", "r", encoding="utf-8") as f:
        local_data = json.load(f)
    local_ver = local_data.get("version", "0.0.0")

    r = requests.get(RAW_VERSION_URL, timeout=10)
    remote_data = r.json()
    remote_ver = remote_data.get("version", "0.0.0")
    changelog = remote_data.get("changelog", [])

    is_new = parse_version(remote_ver) > parse_version(local_ver)
    return local_ver, remote_ver, changelog, is_new


def register(bot):

    @bot.on(events.NewMessage(pattern="/checkupdate"))
    async def checkupdate(event):
        msg = await event.reply("🔍 Checking for updates…")
        try:
            local_ver, remote_ver, changelog, is_new = get_versions()
            if is_new:
                changes = "\n".join(f"• {c}" for c in changelog) or "No details."
                text = f"""🆕 New update available

Current: `{local_ver}`
Latest: `{remote_ver}`

Changes:
{changes}

Type `/update` to install."""
            else:
                text = f"✅ X-OPTIMUS is up to date.\nCurrent version: `{local_ver}`"
            await msg.edit(text)
        except Exception as e:
            await msg.edit(f"❌ Update check failed:\n`{e}`")

    @bot.on(events.NewMessage(pattern="/update"))
    async def do_update(event):
        msg = await event.reply("♻ Checking for updates…")
        try:
            local_ver, remote_ver, changelog, is_new = get_versions()
            if not is_new:
                return await msg.edit(f"✅ Already up to date.\nCurrent version: `{local_ver}`")

            await msg.edit(f"⬇ Updating `{local_ver}` → `{remote_ver}` …")
            os.system("git pull")
            await msg.edit(f"✅ Updated to `{remote_ver}`.\n🔁 Restarting…")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception as e:
            await msg.edit(f"❌ Update failed:\n`{e}`")
