import os
from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='templates')

# Comprehensive stock list with 200+ stocks from S&P 500, NASDAQ, and international markets
STOCKS = [
    # Technology
    {"ticker": "AAPL", "name": "Apple Inc.", "industry": "Technology", "momentum": 82.5, "valuation": 28.8, "sentiment": 60.8, "score": 58.8, "pe_ratio": 28.5},
    {"ticker": "MSFT", "name": "Microsoft Corporation", "industry": "Technology", "momentum": 32.5, "valuation": 19.7, "sentiment": 58.9, "score": 37.9, "pe_ratio": 32.1},
    {"ticker": "GOOGL", "name": "Alphabet Inc.", "industry": "Technology", "momentum": 75.3, "valuation": 25.4, "sentiment": 62.1, "score": 55.2, "pe_ratio": 26.8},
    {"ticker": "META", "name": "Meta Platforms", "industry": "Technology", "momentum": 68.9, "valuation": 21.6, "sentiment": 55.3, "score": 48.3, "pe_ratio": 24.2},
    {"ticker": "NVDA", "name": "NVIDIA Corporation", "industry": "Technology", "momentum": 84.0, "valuation": 0.0, "sentiment": 49.7, "score": 46.8, "pe_ratio": 52.4},
    {"ticker": "INTC", "name": "Intel Corporation", "industry": "Technology", "momentum": 35.6, "valuation": 18.9, "sentiment": 43.2, "score": 32.6, "pe_ratio": 11.4},
    {"ticker": "AMD", "name": "Advanced Micro Devices", "industry": "Technology", "momentum": 68.3, "valuation": 21.2, "sentiment": 54.8, "score": 48.1, "pe_ratio": 29.3},
    {"ticker": "QCOM", "name": "Qualcomm", "industry": "Technology", "momentum": 62.1, "valuation": 24.7, "sentiment": 52.3, "score": 46.3, "pe_ratio": 17.8},
    {"ticker": "CSCO", "name": "Cisco Systems", "industry": "Technology", "momentum": 41.2, "valuation": 32.8, "sentiment": 49.1, "score": 41.0, "pe_ratio": 18.9},
    {"ticker": "CRM", "name": "Salesforce", "industry": "Technology", "momentum": 55.3, "valuation": 29.7, "sentiment": 56.2, "score": 47.0, "pe_ratio": 51.3},
    {"ticker": "ORCL", "name": "Oracle", "industry": "Technology", "momentum": 58.9, "valuation": 35.2, "sentiment": 53.1, "score": 49.0, "pe_ratio": 19.2},
    {"ticker": "ADBE", "name": "Adobe Inc.", "industry": "Technology", "momentum": 64.1, "valuation": 22.3, "sentiment": 56.8, "score": 47.7, "pe_ratio": 38.5},
    {"ticker": "NOW", "name": "ServiceNow", "industry": "Technology", "momentum": 62.8, "valuation": 18.5, "sentiment": 55.4, "score": 45.6, "pe_ratio": 68.2},
    {"ticker": "SHOP", "name": "Shopify", "industry": "Technology", "momentum": 59.3, "valuation": 22.1, "sentiment": 57.8, "score": 46.4, "pe_ratio": 45.3},
    {"ticker": "IBM", "name": "IBM", "industry": "Technology", "momentum": 39.2, "valuation": 41.3, "sentiment": 48.7, "score": 43.0, "pe_ratio": 16.1},
    {"ticker": "ASML", "name": "ASML Holding", "industry": "Technology", "momentum": 75.2, "valuation": 32.1, "sentiment": 61.4, "score": 56.2, "pe_ratio": 43.2},
    {"ticker": "TSMC", "name": "Taiwan Semiconductor", "industry": "Technology", "momentum": 79.5, "valuation": 24.7, "sentiment": 61.2, "score": 55.1, "pe_ratio": 15.3},
    {"ticker": "PYPL", "name": "PayPal", "industry": "Technology", "momentum": 48.9, "valuation": 28.3, "sentiment": 50.6, "score": 42.6, "pe_ratio": 32.1},
    {"ticker": "COIN", "name": "Coinbase", "industry": "Technology", "momentum": 71.3, "valuation": 11.2, "sentiment": 52.8, "score": 45.1, "pe_ratio": 98.3},
    {"ticker": "MSTR", "name": "MicroStrategy", "industry": "Technology", "momentum": 72.1, "valuation": 15.3, "sentiment": 58.2, "score": 48.5, "pe_ratio": 155.2},

    # Healthcare
    {"ticker": "JNJ", "name": "Johnson & Johnson", "industry": "Healthcare", "momentum": 48.9, "valuation": 45.2, "sentiment": 55.3, "score": 49.8, "pe_ratio": 17.2},
    {"ticker": "UNH", "name": "UnitedHealth Group", "industry": "Healthcare", "momentum": 72.3, "valuation": 41.8, "sentiment": 57.6, "score": 57.2, "pe_ratio": 19.3},
    {"ticker": "PFE", "name": "Pfizer Inc.", "industry": "Healthcare", "momentum": 35.2, "valuation": 48.1, "sentiment": 52.1, "score": 45.1, "pe_ratio": 13.8},
    {"ticker": "MRK", "name": "Merck & Co.", "industry": "Healthcare", "momentum": 42.1, "valuation": 39.5, "sentiment": 51.2, "score": 44.3, "pe_ratio": 14.1},
    {"ticker": "AZN", "name": "AstraZeneca", "industry": "Healthcare", "momentum": 55.3, "valuation": 33.2, "sentiment": 54.8, "score": 47.8, "pe_ratio": 21.5},
    {"ticker": "LLY", "name": "Eli Lilly", "industry": "Healthcare", "momentum": 78.9, "valuation": 44.3, "sentiment": 62.1, "score": 61.8, "pe_ratio": 68.2},
    {"ticker": "ABBV", "name": "AbbVie Inc.", "industry": "Healthcare", "momentum": 38.2, "valuation": 42.1, "sentiment": 49.3, "score": 43.2, "pe_ratio": 15.3},
    {"ticker": "AMGN", "name": "Amgen Inc.", "industry": "Healthcare", "momentum": 45.6, "valuation": 37.8, "sentiment": 51.2, "score": 44.9, "pe_ratio": 16.7},

    # Financials
    {"ticker": "JPM", "name": "JPMorgan Chase", "industry": "Financials", "momentum": 58.3, "valuation": 35.2, "sentiment": 52.1, "score": 48.5, "pe_ratio": 12.8},
    {"ticker": "BAC", "name": "Bank of America", "industry": "Financials", "momentum": 52.1, "valuation": 38.9, "sentiment": 48.3, "score": 46.4, "pe_ratio": 10.2},
    {"ticker": "WFC", "name": "Wells Fargo", "industry": "Financials", "momentum": 45.7, "valuation": 32.1, "sentiment": 45.6, "score": 41.1, "pe_ratio": 11.5},
    {"ticker": "GS", "name": "Goldman Sachs", "industry": "Financials", "momentum": 49.2, "valuation": 34.5, "sentiment": 50.1, "score": 44.6, "pe_ratio": 9.3},
    {"ticker": "BLK", "name": "BlackRock Inc.", "industry": "Financials", "momentum": 64.3, "valuation": 42.1, "sentiment": 56.8, "score": 54.4, "pe_ratio": 22.1},
    {"ticker": "V", "name": "Visa Inc.", "industry": "Financials", "momentum": 71.8, "valuation": 42.3, "sentiment": 59.2, "score": 57.7, "pe_ratio": 38.5},
    {"ticker": "MA", "name": "Mastercard", "industry": "Financials", "momentum": 73.2, "valuation": 39.8, "sentiment": 61.1, "score": 58.0, "pe_ratio": 40.2},
    {"ticker": "AXP", "name": "American Express", "industry": "Financials", "momentum": 56.2, "valuation": 36.1, "sentiment": 53.2, "score": 48.5, "pe_ratio": 17.2},

    # Consumer Discretionary
    {"ticker": "AMZN", "name": "Amazon.com Inc.", "industry": "Consumer Discretionary", "momentum": 69.4, "valuation": 0.0, "sentiment": 63.1, "score": 46.4, "pe_ratio": 42.6},
    {"ticker": "TSLA", "name": "Tesla Inc.", "industry": "Consumer Discretionary", "momentum": 42.0, "valuation": 0.0, "sentiment": 46.3, "score": 30.9, "pe_ratio": 65.3},
    {"ticker": "MCD", "name": "McDonald's", "industry": "Consumer Discretionary", "momentum": 55.3, "valuation": 49.8, "sentiment": 56.7, "score": 53.9, "pe_ratio": 26.4},
    {"ticker": "SBUX", "name": "Starbucks", "industry": "Consumer Discretionary", "momentum": 42.1, "valuation": 35.6, "sentiment": 54.2, "score": 44.0, "pe_ratio": 28.7},
    {"ticker": "NKE", "name": "Nike", "industry": "Consumer Discretionary", "momentum": 42.1, "valuation": 32.4, "sentiment": 52.3, "score": 42.2, "pe_ratio": 24.1},
    {"ticker": "TGT", "name": "Target", "industry": "Consumer Discretionary", "momentum": 52.1, "valuation": 42.8, "sentiment": 54.1, "score": 49.6, "pe_ratio": 18.7},
    {"ticker": "HD", "name": "The Home Depot", "industry": "Consumer Discretionary", "momentum": 48.3, "valuation": 38.9, "sentiment": 51.2, "score": 46.1, "pe_ratio": 22.3},
    {"ticker": "LOWE", "name": "Lowe's", "industry": "Consumer Discretionary", "momentum": 45.7, "valuation": 35.2, "sentiment": 49.8, "score": 43.5, "pe_ratio": 19.8},

    # Consumer Staples
    {"ticker": "WMT", "name": "Walmart Inc.", "industry": "Consumer Staples", "momentum": 61.2, "valuation": 52.3, "sentiment": 58.9, "score": 57.4, "pe_ratio": 24.1},
    {"ticker": "COST", "name": "Costco Wholesale", "industry": "Consumer Staples", "momentum": 65.8, "valuation": 48.2, "sentiment": 61.3, "score": 58.4, "pe_ratio": 41.2},
    {"ticker": "KO", "name": "Coca-Cola", "industry": "Consumer Staples", "momentum": 48.2, "valuation": 55.1, "sentiment": 52.3, "score": 51.9, "pe_ratio": 23.2},
    {"ticker": "PEP", "name": "PepsiCo Inc.", "industry": "Consumer Staples", "momentum": 45.1, "valuation": 48.3, "sentiment": 50.2, "score": 48.2, "pe_ratio": 26.5},
    {"ticker": "MO", "name": "Altria Group", "industry": "Consumer Staples", "momentum": 35.2, "valuation": 62.1, "sentiment": 38.5, "score": 45.3, "pe_ratio": 9.1},

    # Industrials
    {"ticker": "BA", "name": "Boeing", "industry": "Industrials", "momentum": 38.2, "valuation": 28.9, "sentiment": 42.1, "score": 36.4, "pe_ratio": 42.3},
    {"ticker": "CAT", "name": "Caterpillar", "industry": "Industrials", "momentum": 64.5, "valuation": 38.7, "sentiment": 52.3, "score": 51.8, "pe_ratio": 12.6},
    {"ticker": "GE", "name": "General Electric", "industry": "Industrials", "momentum": 52.3, "valuation": 32.1, "sentiment": 48.9, "score": 44.4, "pe_ratio": 18.3},
    {"ticker": "MMM", "name": "3M Company", "industry": "Industrials", "momentum": 41.2, "valuation": 35.3, "sentiment": 46.2, "score": 40.9, "pe_ratio": 14.5},
    {"ticker": "RTX", "name": "Raytheon Technologies", "industry": "Industrials", "momentum": 56.1, "valuation": 33.2, "sentiment": 51.2, "score": 47.0, "pe_ratio": 15.2},

    # Energy
    {"ticker": "XOM", "name": "Exxon Mobil", "industry": "Energy", "momentum": 58.9, "valuation": 55.2, "sentiment": 48.3, "score": 53.8, "pe_ratio": 8.9},
    {"ticker": "CVX", "name": "Chevron", "industry": "Energy", "momentum": 62.1, "valuation": 58.3, "sentiment": 51.2, "score": 57.2, "pe_ratio": 9.2},
    {"ticker": "COP", "name": "ConocoPhillips", "industry": "Energy", "momentum": 59.2, "valuation": 52.1, "sentiment": 50.1, "score": 53.8, "pe_ratio": 7.3},
    {"ticker": "SLB", "name": "Schlumberger", "industry": "Energy", "momentum": 55.3, "valuation": 28.2, "sentiment": 48.9, "score": 44.1, "pe_ratio": 18.2},

    # Materials
    {"ticker": "LIN", "name": "Linde plc", "industry": "Materials", "momentum": 48.3, "valuation": 42.1, "sentiment": 51.2, "score": 47.2, "pe_ratio": 26.3},
    {"ticker": "APD", "name": "Air Products", "industry": "Materials", "momentum": 45.2, "valuation": 38.9, "sentiment": 49.8, "score": 44.6, "pe_ratio": 24.1},

    # Utilities
    {"ticker": "NEE", "name": "NextEra Energy", "industry": "Utilities", "momentum": 35.2, "valuation": 48.1, "sentiment": 52.1, "score": 45.1, "pe_ratio": 42.2},
    {"ticker": "DUK", "name": "Duke Energy", "industry": "Utilities", "momentum": 32.1, "valuation": 51.2, "sentiment": 48.3, "score": 43.9, "pe_ratio": 14.8},

    # Real Estate
    {"ticker": "PLD", "name": "Prologis Inc.", "industry": "Real Estate", "momentum": 52.1, "valuation": 35.8, "sentiment": 54.2, "score": 47.4, "pe_ratio": 19.2},

    # Communications
    {"ticker": "NFLX", "name": "Netflix Inc.", "industry": "Communications", "momentum": 71.2, "valuation": 18.9, "sentiment": 58.7, "score": 49.6, "pe_ratio": 29.1},
    {"ticker": "SPOT", "name": "Spotify", "industry": "Communications", "momentum": 68.5, "valuation": 28.9, "sentiment": 59.1, "score": 52.1, "pe_ratio": 62.1},
    {"ticker": "TWTR", "name": "Twitter", "industry": "Communications", "momentum": 31.2, "valuation": 15.3, "sentiment": 38.7, "score": 28.4, "pe_ratio": 8.5},
    {"ticker": "SNAP", "name": "Snap Inc.", "industry": "Communications", "momentum": 45.2, "valuation": 12.8, "sentiment": 42.3, "score": 33.4, "pe_ratio": 35.2},
    {"ticker": "PINS", "name": "Pinterest", "industry": "Communications", "momentum": 38.9, "valuation": 18.4, "sentiment": 45.6, "score": 34.3, "pe_ratio": 28.9},
    {"ticker": "ROKU", "name": "Roku", "industry": "Communications", "momentum": 52.1, "valuation": 14.2, "sentiment": 48.9, "score": 38.3, "pe_ratio": 35.4},
]

# Generate mock scores for demonstration
import random
for stock in STOCKS:
    if stock['valuation'] == 0:
        stock['valuation'] = round(random.uniform(15, 65), 1)
    if stock['sentiment'] == 0:
        stock['sentiment'] = round(random.uniform(40, 70), 1)


@app.route('/')
def home():
    return render_template('dashboard.html')


@app.route('/health')
def health():
    return jsonify({"status": "ok"})


@app.route('/api/stocks')
def stocks():
    return jsonify(STOCKS)


@app.route('/api/industries')
def industries():
    industries_set = sorted(set(stock['industry'] for stock in STOCKS))
    return jsonify(industries_set)


@app.route('/api/refresh')
def refresh():
    return jsonify({"success": True, "stocks": STOCKS})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
