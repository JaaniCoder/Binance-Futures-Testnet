# Binance Futures Trading Bot 🚀

An interactive Python trading bot for **Binance Futures Testnet**, supporting:

- Market Orders
- Limit Orders
- Stop-Market Orders
- OCO Orders (Take-Profit + Stop-Loss)
- Rich CLI with colored tables
- View Positions & Open Orders

## ⚡ Features
- Built with [binance-futures-connector](https://pypi.org/project/binance-futures-connector/)  
- Interactive CLI menu for easy trading  
- OCO support for safer trading  

## 🔧 Installation

```
git clone https://github.com/<your-username>/binance-futures-trading-bot.git
cd binance-futures-trading-bot
python -m venv venv
venv\Scripts\activate   # (Windows)
pip install -r requirements.txt
```

## ▶️ Run

```
python -m trading_bot.cli --interactive
```

## 🛠️ Example

```
=== Interactive Trading Bot ===
1. Market Order
2. Limit Order
3. Stop-Market Order
4. OCO Order
5. View Positions
6. View Open Orders
7. Exit
```

## ⚠️ Disclaimer
This bot is for educational purposes only and runs on the Binance Testnet.
Do not use with real funds without thorough testing.

---

## 🔹 Add your files to Git

```
git add .
git commit -m "Initial commit: Binance Futures Trading Bot with Rich CLI"
```

---

## 🔹 Connect to GitHub
Replace <your-username> with your GitHub username:

```
git remote add origin https://github.com/<your-username>/binance-futures-trading-bot.git
git branch -M main
git push -u origin main
```

## 🔹 Verify
Go to your repo URL, refresh, and you should see your code + README.