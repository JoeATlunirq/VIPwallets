# 🎯 Vanity Solana Wallet Generator

Generate Solana wallets until one is found where the **public address** starts or ends with a custom phrase (like `"wife"` or `"wifey"`). When a match is found, display the wallet details.

---

## 📁 Project Structure

```
vanity-wallet/
├── backend/
│   └── generator.py
├── frontend/
│   └── index.html
├── app.py           # Flask entry point
└── requirements.txt
```

---

## 🔧 Tech Stack

- **Backend**: Python, Flask, `solana-py`, `base58`
- **Frontend**: Plain HTML + JavaScript (no framework needed)
- **Optional**: Multithreading with `multiprocessing`

---

## ⚙️ Backend Logic

`generator.py` will:

1. Accept a target phrase.
2. Continuously generate Solana wallets.
3. Check if the public key starts or ends with the phrase.
4. Return the matched wallet info when found.

> 🔐 Output includes:  
> - Public key  
> - Base58 private key  
> - Match type (prefix/suffix)

---

## 🧪 Example Flask API

```python
# app.py
from flask import Flask, request, jsonify
from solana.keypair import Keypair
import base58
import threading

app = Flask(__name__)
stop_flag = threading.Event()

def search_wallet(target, callback):
    target = target.lower()
    while not stop_flag.is_set():
        keypair = Keypair.generate()
        pubkey = str(keypair.public_key).lower()
        if pubkey.startswith(target) or pubkey.endswith(target):
            privkey_b58 = base58.b58encode(keypair.secret_key).decode()
            callback({
                "public_key": pubkey,
                "private_key": privkey_b58,
                "match_type": "prefix" if pubkey.startswith(target) else "suffix"
            })
            break

@app.route("/start", methods=["POST"])
def start():
    data = request.json
    target = data.get("target")
    if not target:
        return {"error": "Missing target"}, 400

    stop_flag.clear()

    def send_result(result):
        global match_result
        match_result = result
        stop_flag.set()

    thread = threading.Thread(target=search_wallet, args=(target, send_result))
    thread.start()

    return {"status": "searching"}

@app.route("/status")
def status():
    if stop_flag.is_set():
        return jsonify(match_result)
    return {"status": "searching"}

@app.route("/stop")
def stop():
    stop_flag.set()
    return {"status": "stopped"}

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 💻 Frontend UI (HTML + JS)

`frontend/index.html`

```html
<!DOCTYPE html>
<html>
<head>
  <title>Solana Vanity Wallet</title>
</head>
<body>
  <h1>🔍 Find a Solana Wallet</h1>
  <input id="phrase" placeholder="Enter phrase (e.g. wife)" />
  <button onclick="start()">Start</button>
  <button onclick="stop()">Stop</button>
  <p id="status">Status: Idle</p>
  <pre id="result"></pre>

  <script>
    let interval;

    function start() {
      const phrase = document.getElementById('phrase').value;
      fetch("/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target: phrase })
      });

      document.getElementById("status").textContent = "Status: Searching...";
      interval = setInterval(checkStatus, 2000);
    }

    function checkStatus() {
      fetch("/status").then(res => res.json()).then(data => {
        if (data.public_key) {
          clearInterval(interval);
          document.getElementById("status").textContent = "✅ Match Found!";
          document.getElementById("result").textContent = JSON.stringify(data, null, 2);
        }
      });
    }

    function stop() {
      fetch("/stop");
      clearInterval(interval);
      document.getElementById("status").textContent = "⏹️ Stopped.";
    }
  </script>
</body>
</html>
```

---

## 📦 requirements.txt

```
flask
solana
base58
```

---

## 🚀 Run the App

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Start Flask:
    ```bash
    python app.py
    ```

3. Open `frontend/index.html` in your browser (or serve via Flask static folder if needed).

---

## ✅ When Match is Found

The frontend will display:

```json
{
  "public_key": "wifeXo29uQYZ...",
  "private_key": "3Dk8wGmL5kUt...etc",
  "match_type": "prefix"
}
```

---

## 🔐 Security Tip

This is for **educational / testing** use only. If you're generating real wallets for money:

- Don't expose the backend to the public internet.
- Never log or share private keys.
- Use encryption for storing keys securely.

---

## 🛠 Optional Improvements

- Add multithreading for faster generation
- Show live generation rate
- Let user choose `"starts with"`, `"ends with"`, or `"contains"`
- Add export/download button for matched wallet
