# webserver.py
from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "X-OPTIMUS RUNNING ✔"

def run():
    port = int(os.environ.get("PORT", 8080))
    print(f"[WebServer] Starting on port {port}...")
    app.run(host="0.0.0.0", port=port)

def start_webserver():
    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()
