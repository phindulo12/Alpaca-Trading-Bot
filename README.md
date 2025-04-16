
# 📈 Alpaca SMA Trading Bot

This is a simple yet powerful trading bot written in Python that uses Alpaca's API to trade stocks based on a **Simple Moving Average (SMA) crossover strategy**. The bot automatically fetches data, generates buy/sell signals, and executes trades accordingly.

---

## 🔧 Features

- ✅ Connects to Alpaca paper/live trading accounts  
- 📊 Implements **SMA Crossover Strategy**  
- 💵 Automatically calculates quantity to trade based on a fixed dollar amount  
- 📈 Trades real stocks like `AAPL`, `TSLA`, etc.  
- 🕒 Checks market hours before placing trades (can override for testing)  
- 🧠 Strategy logic modular and extendable  
- 📋 Clean logging with error handling  
- 🔁 Continuous loop with retry mechanism

---

## 📁 Files

| File | Description |
|------|-------------|
| `trading_bot.py` | Main script containing the `TradingBot` class |
| `README.md` | This documentation file |

---

## 🚀 Getting Started

### 1. **Install Dependencies**

Make sure you have Python 3.7+ installed.

```bash
pip install alpaca-trade-api pandas
```

### 2. **Get Your Alpaca API Keys**

Create an account on [https://alpaca.markets](https://alpaca.markets) and generate your API key and secret (use **paper trading** keys for testing).

### 3. **Update API Credentials**

Edit the bottom of `trading_bot.py`:

```python
API_KEY = 'YOUR_ALPACA_API_KEY'
API_SECRET = 'YOUR_ALPACA_API_SECRET'
```

---

## ⚙️ How It Works

### 📌 Strategy: Simple Moving Average Crossover

- **Short SMA (default: 20 periods)** crosses above **Long SMA (default: 50)** → **Buy**
- **Short SMA** crosses below **Long SMA** → **Sell**
- Otherwise → **Hold**

### 💡 Sample Run:

```python
bot = TradingBot(API_KEY, API_SECRET)
bot.run_bot('AAPL', strategy='sma', force_trade=True)
```

- `symbol`: Stock to trade (e.g., `'AAPL'`)
- `strategy`: Strategy to use (`'sma'` supported)
- `force_trade`: Run even if market is closed (for testing)

---

## 📈 Example Log Output

```
INFO - Initialized trading bot for account PAPER12345678
INFO - Starting trading bot for AAPL...
INFO - Strategy signal for AAPL: buy
INFO - Calculated qty to buy: 3
INFO - Placing buy order for 3 shares of AAPL
INFO - Order placed: 12345678-abcd-efgh
```

---

## 🔐 Safety Notice

- This bot places **real trades** if used with a live account.
- Always test thoroughly with **paper trading**.
- Monitor trading activity to avoid unintended losses.

---

## 🛠️ Future Improvements

- Add advanced strategies like RSI, MACD, or Bollinger Bands  
- Enable email/Telegram notifications for trades  
- Web dashboard to monitor trades and performance  
- Add a backtesting module

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

## 🙋‍♂️ Questions?

Feel free to reach out if you need help customizing or extending the bot!
