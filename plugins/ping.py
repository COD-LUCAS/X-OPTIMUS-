import psutil, platform, time
from telethon import events, version

def register(bot):
    @bot.on(events.NewMessage(pattern="/ping"))
    async def _(event):
        start = time.time()
        msg = await event.reply("⏳")
        ping_ms = int((time.time() - start) * 1000)

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent

        boot = psutil.boot_time()
        uptime_sec = int(time.time() - boot)
        h = uptime_sec // 3600
        m = (uptime_sec % 3600) // 60
        uptime = f"{h}h {m}m"

        os_info = f"{platform.system()} {platform.release()}"
        tele = version.__version__

        net1 = psutil.net_io_counters().bytes_sent, psutil.net_io_counters().bytes_recv
        time.sleep(1)
        net2 = psutil.net_io_counters().bytes_sent, psutil.net_io_counters().bytes_recv
        upload = (net2[0] - net1[0]) / 1024
        download = (net2[1] - net1[1]) / 1024

        caption = (
            "⚡ **X-OPTIMUS REAL PING REPORT** ⚡\n\n"
            f"🏓 **Ping:** `{ping_ms} ms`\n"
            f"🧠 **CPU:** `{cpu}%`\n"
            f"💾 **RAM:** `{ram}%`\n"
            f"🗂 **Disk:** `{disk}%`\n"
            f"📤 **Upload:** `{upload:.1f} KB/s`\n"
            f"📥 **Download:** `{download:.1f} KB/s`\n"
            f"⏱ **Uptime:** `{uptime}`\n"
            f"🛠 **OS:** `{os_info}`\n"
            f"📡 **Telethon:** `{tele}`"
        )

        try:
            await event.client.send_file(
                event.chat_id,
                "assets/ping.jpg",
                caption=caption,
                reply_to=event.id
            )
            await msg.delete()
        except:
            await msg.edit(caption)
