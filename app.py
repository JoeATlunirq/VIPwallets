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

<<<<<<< HEAD
def search_wallet_batch(target, batch_size=25000):
=======
def search_wallet_batch(target, position='any', case_sensitive=False, batch_size=25000):
>>>>>>> f9cebdb (feat: update token contract address)
    """
    Generates a large batch of wallets and checks for a match.
    This is a short-lived, stateless function for serverless environments.
    It returns the exact number of attempts performed in this batch.
    """
    attempts_in_batch = 0
    recent_wallets = []
    
<<<<<<< HEAD
=======
    # Adjust target based on case sensitivity
    comparison_target = target if case_sensitive else target.lower()

>>>>>>> f9cebdb (feat: update token contract address)
    for _ in range(batch_size):
        keypair = Keypair()
        pubkey = str(keypair.pubkey())
        attempts_in_batch += 1
        
<<<<<<< HEAD
=======
        # Adjust pubkey for comparison based on case sensitivity
        comparison_pubkey = pubkey if case_sensitive else pubkey.lower()

>>>>>>> f9cebdb (feat: update token contract address)
        # Add a recent wallet to the list periodically for display
        if attempts_in_batch % 2500 == 0:
             recent_wallets.append(pubkey)

<<<<<<< HEAD
        if pubkey.lower().startswith(target) or pubkey.lower().endswith(target):
=======
        match_found = False
        match_type = None

        if position == 'start' and comparison_pubkey.startswith(comparison_target):
            match_found = True
            match_type = 'prefix'
        elif position == 'end' and comparison_pubkey.endswith(comparison_target):
            match_found = True
            match_type = 'suffix'
        elif position == 'any':
            if comparison_pubkey.startswith(comparison_target):
                match_found = True
                match_type = 'prefix'
            elif comparison_pubkey.endswith(comparison_target):
                match_found = True
                match_type = 'suffix'

        if match_found:
>>>>>>> f9cebdb (feat: update token contract address)
            privkey_b58 = base58.b58encode(bytes(keypair)).decode()
            return {
                "found": True,
                "public_key": pubkey,
                "private_key": privkey_b58,
<<<<<<< HEAD
                "match_type": "prefix" if pubkey.lower().startswith(target) else "suffix",
=======
                "match_type": match_type,
>>>>>>> f9cebdb (feat: update token contract address)
                "attempts": attempts_in_batch,
                "recent_wallets": recent_wallets
            }
            
    # If no match is found in the batch
    return {
        "found": False,
        "attempts": attempts_in_batch,
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
<<<<<<< HEAD

    if not target or not isinstance(target, str) or not (1 <= len(target) <= 10):
        return {"error": "Invalid target specified."}, 400

    result = search_wallet_batch(target.lower())
=======
    position = data.get("position", "any")  # 'start', 'end', or 'any'
    case_sensitive = data.get("case_sensitive", False)

    if not target or not isinstance(target, str) or not (1 <= len(target) <= 10):
        return {"error": "Invalid target specified."}, 400
    
    if position not in ['start', 'end', 'any']:
        return {"error": "Invalid position specified."}, 400

    result = search_wallet_batch(target, position, case_sensitive)
>>>>>>> f9cebdb (feat: update token contract address)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000) 