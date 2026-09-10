import os
import json
from flask import Flask, render_template, jsonify
import logging

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates')

def load_stocks_data():
    """Load stock data from JSON file (populated from Shibui Finance)"""
    try:
        data_file = os.path.join(os.path.dirname(__file__), 'stocks_data.json')
        if os.path.exists(data_file):
            with open(data_file, 'r') as f:
                data = json.load(f)
                if data.get('stocks'):
                    logger.info(f"Loaded {len(data['stocks'])} stocks from Shibui Finance data")
                    return data['stocks']
    except Exception as e:
        logger.error(f"Error loading stocks data: {e}")

    logger.warning("No real stock data available - please populate stocks_data.json")
    return []

STOCKS = load_stocks_data()

def fetch_yahoo_stock(ticker):
    """Fetch live stock data from Yahoo Finance"""
    try:
        data = yf.Ticker(ticker)
        info = data.info

        price = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        target = info.get('targetMeanPrice') or price * 1.1
        pe = info.get('trailingPE') or info.get('forwardPE') or 20
        market_cap = info.get('marketCap', 0) / 1e9
        dividend = info.get('dividendRate', 0) or (info.get('dividendYield', 0) * price if price > 0 else 0)
        low_52w = info.get('fiftyTwoWeekLow', price * 0.8)
        high_52w = info.get('fiftyTwoWeekHigh', price * 1.2)
        name = info.get('longName', ticker)
        sector = info.get('sector', 'Technology')

        if price > 0:
            upside = ((target - price) / price * 100)
            momentum = min(95, 50 + upside / 2)
            valuation = 85 if pe < 15 else (70 if pe < 25 else (55 if pe < 40 else 40))
            sentiment = min(95, 50 + upside / 3)
            score = (momentum + valuation + sentiment) / 3

            return {
                "ticker": ticker,
                "name": name,
                "industry": sector,
                "price": round(price, 2),
                "target": round(target, 2),
                "upside": round(upside, 1),
                "low_52w": round(low_52w, 2),
                "high_52w": round(high_52w, 2),
                "market_cap": round(market_cap, 1),
                "dividend": round(dividend, 2),
                "pe_ratio": round(pe, 2),
                "analysts": [{"name": "Yahoo Finance", "rating": "BUY" if upside > 15 else ("HOLD" if upside > 0 else "SELL"), "target": round(target, 2)}],
                "momentum": round(momentum, 1),
                "valuation": round(valuation, 1),
                "sentiment": round(sentiment, 1),
                "score": round(score, 1),
                "headlines": []
            }
    except Exception as e:
        logger.error(f"Error fetching {ticker}: {e}")
    return None

def fetch_all_yahoo_stocks(tickers):
    """Fetch data for multiple tickers"""
    stocks = []
    for ticker in tickers:
        stock = fetch_yahoo_stock(ticker)
        if stock:
            stocks.append(stock)
    stocks.sort(key=lambda x: x['ticker'])
    return stocks

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/api/stocks')
def stocks():
    return jsonify(STOCKS)

@app.route('/api/refresh')
def refresh():
    global STOCKS
    STOCKS = load_stocks_data()
    return jsonify({"success": True, "stocks": STOCKS})

@app.route('/api/stocks/live')
def stocks_live():
    """Fetch live stock data from Yahoo Finance"""
    if not YFINANCE_AVAILABLE:
        logger.warning("yfinance not available, falling back to cached data")
        return jsonify(STOCKS)

    tickers = [
        "AAPL", "MSFT", "NVDA", "GOOGL", "META", "AMZN", "TSLA", "JPM", "V", "JNJ",
        "WMT", "PG", "NFLX", "DIS", "ADBE", "CRM", "ORCL", "INTC", "AMD", "CSCO",
        "QCOM", "PYPL", "MA", "ABT", "KO", "PFE", "XOM", "CVX", "WFC", "BAC",
        "GS", "MS", "SCHW", "COIN", "SHOP", "AKAM", "NKE", "SBUX", "MCD", "ABNB"
    ]

    live_stocks = fetch_all_yahoo_stocks(tickers)
    if live_stocks:
        logger.info(f"Fetched {len(live_stocks)} live stocks from Yahoo Finance")
        return jsonify(live_stocks)

    logger.warning("Failed to fetch live data, using cached stocks")
    return jsonify(STOCKS)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
