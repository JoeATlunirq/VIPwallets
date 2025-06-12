# VIP Wallet - Solana Vanity Address Generator

Generate custom Solana wallet addresses with your desired prefix or suffix.

## Features

- 🎯 Generate wallets with custom prefixes or suffixes
- ⚡ Real-time performance statistics
- 🕐 Live countdown timer with time estimates
- 💎 Beautiful Solana-themed UI
- 📱 Fully responsive design
- 🔒 Secure key generation using solders library

## Live Demo

Visit [VIPWallet.fun](https://vipwallet.fun) to try it out!

## Local Development

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/JoeATlunirq/VIPwallets.git
cd VIPwallets
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Deployment

This project is configured for easy deployment on Vercel:

1. Fork this repository
2. Connect your GitHub account to Vercel
3. Import this repository
4. Deploy!

The `vercel.json` configuration file is already set up for proper routing and static file serving.

## How It Works

The application uses a brute-force approach to generate Solana keypairs until it finds one matching your desired pattern. The backend is built with Flask and uses the `solders` library for efficient keypair generation.

### Performance

- Generates thousands of wallets per second
- Performance depends on your CPU
- Longer phrases take exponentially longer to find

### Security

- All keys are generated locally
- No keys are stored or transmitted
- Use at your own risk - always verify keys before use

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Crypto**: solders (Solana keypair generation)
- **Deployment**: Vercel

## License

MIT License - see [LICENSE](LICENSE) file for details

## Disclaimer

This tool is for educational and entertainment purposes. Always verify generated keys and use proper security practices when handling cryptocurrency wallets. 