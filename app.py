# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from solders.keypair import Keypair
import base58
import threading
import os
import time
from collections import deque

# Configure Flask app with explicit static handling
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Global state
stop_flag = threading.Event()
match_result = None
attempts = 0
start_time = 0
wallets_per_second = 0
recent_wallets = deque(maxlen=10)

def search_wallet(target, callback):
    global attempts
    target = target.lower()
    while not stop_flag.is_set():
        keypair = Keypair()
        pubkey = str(keypair.pubkey())
        attempts += 1
        recent_wallets.append(pubkey)
        
        if pubkey.lower().startswith(target) or pubkey.lower().endswith(target):
            privkey_b58 = base58.b58encode(bytes(keypair)).decode()
            callback({
                "public_key": pubkey,
                "private_key": privkey_b58,
                "match_type": "prefix" if pubkey.lower().startswith(target) else "suffix"
            })
            break

def stats_updater():
    global wallets_per_second
    last_attempts = 0
    while not stop_flag.is_set():
        time.sleep(1)
        if start_time > 0:
            current_attempts = attempts
            wallets_per_second = current_attempts - last_attempts
            last_attempts = current_attempts

@app.route("/")
def index():
    return send_from_directory('frontend', 'index.html')

# Explicit routes for static files to ensure Vercel compatibility
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('frontend', 'favicon.ico')

@app.route('/logo-bg.png')
def logo_bg():
    return send_from_directory('frontend', 'logo-bg.png')

@app.route('/background.png')
def background():
    return send_from_directory('frontend', 'background.png')

@app.route('/logo.png')
def logo():
    return send_from_directory('frontend', 'logo.png')

@app.route("/start", methods=["POST"])
def start():
    global match_result, attempts, start_time, wallets_per_second, recent_wallets
    data = request.json
    target = data.get("target")
    if not target:
        return {"error": "Missing target"}, 400

    stop_flag.clear()
    match_result = None
    attempts = 0
    start_time = time.time()
    wallets_per_second = 0
    recent_wallets.clear()

    def send_result(result):
        global match_result
        match_result = result
        stop_flag.set()

    search_thread = threading.Thread(target=search_wallet, args=(target, send_result))
    search_thread.daemon = True
    search_thread.start()

    stats_thread = threading.Thread(target=stats_updater)
    stats_thread.daemon = True
    stats_thread.start()

    return {"status": "searching"}

@app.route("/stats")
def stats():
    elapsed_time = 0
    if start_time > 0:
        elapsed_time = time.time() - start_time
        
    return jsonify({
        "wps": wallets_per_second,
        "attempts": attempts,
        "elapsed_time": elapsed_time,
        "recent_wallets": list(recent_wallets)
    })

@app.route("/status")
def status():
    if stop_flag.is_set() and match_result:
        return jsonify(match_result)
    return {"status": "searching"}

@app.route("/stop")
def stop():
    global start_time
    stop_flag.set()
    start_time = 0
    return {"status": "stopped"}

if __name__ == "__main__":
    app.run(debug=True, port=5000) 