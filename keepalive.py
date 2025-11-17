from flask import Flask
import threading

app = Flask('XOPTIMUS')

@app.route('/')
def home():
    return "X-OPTIMUS USERBOT ACTIVE"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()
