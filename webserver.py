from flask import Flask
from threading import Thread
import requests
import time
import os

app = Flask(__name__)

AUTO_URL = None

@app.route("/")
def home():
    return "Bot Alive"

# ---------------------------------------------------
# 🔥 AUTO FETCH PUBLIC URL (Render)
# ---------------------------------------------------
def detect_render_url():
    global AUTO_URL

    # 1) Render provides service URL in env (sometimes)
    if os.getenv("RENDER_EXTERNAL_URL"):
        AUTO_URL = os.getenv("RENDER_EXTERNAL_URL")
        return AUTO_URL

    # 2) Render Metadata API (works for MANY users)
    try:
        meta = requests.get(
            "http://100.100.100.100/metadata",
            headers={"Metadata-Flavor": "Google"},
            timeout=3
        ).json()

        if "service" in meta and "url" in meta["service"]:
            AUTO_URL = meta["service"]["url"]
            return AUTO_URL
    except:
        pass

    # 3) Try to detect Render domain (fallback guessing)
    try:
        app_name = os.getenv("RENDER_SERVICE_NAME")
        if app_name:
            AUTO_URL = f"https://{app_name}.onrender.com"
            return AUTO_URL
    except:
        pass

    # 4) If everything fails
    AUTO_URL = ""
    return ""


# ---------------------------------------------------
# 🔄 AUTO SELF-PINGER (Prevents Render Free Sleep)
# ---------------------------------------------------
def self_ping():
    global AUTO_URL
    time.sleep(5)  # wait for URL detection

    while True:
        if not AUTO_URL:
            detect_render_url()

        if AUTO_URL:
            try:
                requests.get(AUTO_URL)
                print("🔄 Self-Ping Success →", AUTO_URL)
            except Exception as e:
                print("❌ Self-Ping Failed:", e)
        else:
            print("⚠ No URL detected yet.")

        time.sleep(240)  # ping every 4 minutes


# ---------------------------------------------------
# 🚀 START KEEP-ALIVE SYSTEM
# ---------------------------------------------------
def keep_alive():
    Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()
    Thread(target=self_ping).start()
