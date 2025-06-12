# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from solders.keypair import Keypair
import base58
import os
import time

# Configure Flask app
app = Flask(__name__, static_folder='frontend')
CORS(app)  # Enable CORS for frontend communication

# This is a stateless function. It will run for a short duration
# and then return, fitting within serverless execution limits.
def search_wallet_batch(target, batch_size=25000):
    """
    Generates a batch of wallets and checks for a match.
    This is designed to be a short-lived, stateless function.
    """
    attempts = 0
    recent_wallets = []
    
    for i in range(batch_size):
        keypair = Keypair()
        pubkey = str(keypair.pubkey())
        attempts += 1
        if i % 2500 == 0: # Add a recent wallet every so often
             recent_wallets.append(pubkey)

        if pubkey.lower().startswith(target) or pubkey.lower().endswith(target):
            privkey_b58 = base58.b58encode(bytes(keypair)).decode()
            return {
                "found": True,
                "public_key": pubkey,
                "private_key": privkey_b58,
                "match_type": "prefix" if pubkey.lower().startswith(target) else "suffix",
                "attempts": attempts,
                "recent_wallets": recent_wallets
            }
            
    # If no match is found in the batch
    return {
        "found": False,
        "attempts": attempts,
        "recent_wallets": recent_wallets
    }


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/api/generate_batch", methods=["POST"])
def generate_batch_route():
    data = request.json
    target = data.get("target")

    if not target or not isinstance(target, str) or not (1 <= len(target) <= 10):
        return {"error": "Invalid target specified."}, 400

    result = search_wallet_batch(target.lower())
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000) 