import os
import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='templates')

# NewsAPI key from environment
NEWS_API_KEY = os.environ.get('NEWS_API_KEY', '96eb0f8f345140ecbf244a1edbc63039')

STOCKS = [
    {"ticker": "AAPL", "name": "Apple Inc.", "momentum": 82.5, "valuation": 28.8, "sentiment": 60.8, "score": 58.8, "pe_ratio": 28.5},
    {"ticker": "NVDA", "name": "NVIDIA Corporation", "momentum": 84.0, "valuation": 0.0, "sentiment": 49.7, "score": 46.8, "pe_ratio": 52.4},
    {"ticker": "AMZN", "name": "Amazon.com Inc.", "momentum": 69.4, "valuation": 0.0, "sentiment": 63.1, "score": 46.4, "pe_ratio": 42.6},
    {"ticker": "MSFT", "name": "Microsoft Corporation", "momentum": 32.5, "valuation": 19.7, "sentiment": 58.9, "score": 37.9, "pe_ratio": 32.1},
    {"ticker": "TSLA", "name": "Tesla Inc.", "momentum": 42.0, "valuation": 0.0, "sentiment": 46.3, "score": 30.9, "pe_ratio": 65.3},
    {"ticker": "GOOGL", "name": "Alphabet Inc.", "momentum": 75.3, "valuation": 25.4, "sentiment": 62.1, "score": 55.2, "pe_ratio": 26.8},
    {"ticker": "META", "name": "Meta Platforms", "momentum": 68.9, "valuation": 21.6, "sentiment": 55.3, "score": 48.3, "pe_ratio": 24.2},
    {"ticker": "NFLX", "name": "Netflix Inc.", "momentum": 71.2, "valuation": 18.9, "sentiment": 58.7, "score": 49.6, "pe_ratio": 29.1},
    {"ticker": "ADOBE", "name": "Adobe Inc.", "momentum": 64.1, "valuation": 22.3, "sentiment": 56.8, "score": 47.7, "pe_ratio": 38.5},
    {"ticker": "TSMC", "name": "Taiwan Semiconductor", "momentum": 79.5, "valuation": 24.7, "sentiment": 61.2, "score": 55.1, "pe_ratio": 15.3},
    {"ticker": "JPM", "name": "JPMorgan Chase", "momentum": 58.3, "valuation": 35.2, "sentiment": 52.1, "score": 48.5, "pe_ratio": 12.8},
    {"ticker": "BAC", "name": "Bank of America", "momentum": 52.1, "valuation": 38.9, "sentiment": 48.3, "score": 46.4, "pe_ratio": 10.2},
    {"ticker": "WFC", "name": "Wells Fargo", "momentum": 45.7, "valuation": 32.1, "sentiment": 45.6, "score": 41.1, "pe_ratio": 11.5},
    {"ticker": "JNJ", "name": "Johnson & Johnson", "momentum": 48.9, "valuation": 45.2, "sentiment": 55.3, "score": 49.8, "pe_ratio": 17.2},
    {"ticker": "UNH", "name": "UnitedHealth Group", "momentum": 72.3, "valuation": 41.8, "sentiment": 57.6, "score": 57.2, "pe_ratio": 19.3},
    {"ticker": "PFE", "name": "Pfizer Inc.", "momentum": 35.2, "valuation": 48.1, "sentiment": 52.1, "score": 45.1, "pe_ratio": 13.8},
    {"ticker": "WMT", "name": "Walmart Inc.", "momentum": 61.2, "valuation": 52.3, "sentiment": 58.9, "score": 57.4, "pe_ratio": 24.1},
    {"ticker": "COST", "name": "Costco Wholesale", "momentum": 65.8, "valuation": 48.2, "sentiment": 61.3, "score": 58.4, "pe_ratio": 41.2},
    {"ticker": "MCD", "name": "McDonald's", "momentum": 55.3, "valuation": 49.8, "sentiment": 56.7, "score": 53.9, "pe_ratio": 26.4},
    {"ticker": "SBUX", "name": "Starbucks", "momentum": 42.1, "valuation": 35.6, "sentiment": 54.2, "score": 44.0, "pe_ratio": 28.7},
    {"ticker": "XOM", "name": "Exxon Mobil", "momentum": 58.9, "valuation": 55.2, "sentiment": 48.3, "score": 53.8, "pe_ratio": 8.9},
    {"ticker": "CVX", "name": "Chevron", "momentum": 62.1, "valuation": 58.3, "sentiment": 51.2, "score": 57.2, "pe_ratio": 9.2},
    {"ticker": "BA", "name": "Boeing", "momentum": 38.2, "valuation": 28.9, "sentiment": 42.1, "score": 36.4, "pe_ratio": 42.3},
    {"ticker": "CAT", "name": "Caterpillar", "momentum": 64.5, "valuation": 38.7, "sentiment": 52.3, "score": 51.8, "pe_ratio": 12.6},
    {"ticker": "GE", "name": "General Electric", "momentum": 52.3, "valuation": 32.1, "sentiment": 48.9, "score": 44.4, "pe_ratio": 18.3},
    {"ticker": "V", "name": "Visa Inc.", "momentum": 71.8, "valuation": 42.3, "sentiment": 59.2, "score": 57.7, "pe_ratio": 38.5},
    {"ticker": "MA", "name": "Mastercard", "momentum": 73.2, "valuation": 39.8, "sentiment": 61.1, "score": 58.0, "pe_ratio": 40.2},
    {"ticker": "PYPL", "name": "PayPal", "momentum": 48.9, "valuation": 28.3, "sentiment": 50.6, "score": 42.6, "pe_ratio": 32.1},
    {"ticker": "INTC", "name": "Intel", "momentum": 35.6, "valuation": 18.9, "sentiment": 43.2, "score": 32.6, "pe_ratio": 11.4},
    {"ticker": "AMD", "name": "Advanced Micro Devices", "momentum": 68.3, "valuation": 21.2, "sentiment": 54.8, "score": 48.1, "pe_ratio": 29.3},
    {"ticker": "QCOM", "name": "Qualcomm", "momentum": 62.1, "valuation": 24.7, "sentiment": 52.3, "score": 46.3, "pe_ratio": 17.8},
    {"ticker": "CSCO", "name": "Cisco Systems", "momentum": 41.2, "valuation": 32.8, "sentiment": 49.1, "score": 41.0, "pe_ratio": 18.9},
    {"ticker": "CRM", "name": "Salesforce", "momentum": 55.3, "valuation": 29.7, "sentiment": 56.2, "score": 47.0, "pe_ratio": 51.3},
    {"ticker": "ORCL", "name": "Oracle", "momentum": 58.9, "valuation": 35.2, "sentiment": 53.1, "score": 49.0, "pe_ratio": 19.2},
    {"ticker": "IBM", "name": "IBM", "momentum": 39.2, "valuation": 41.3, "sentiment": 48.7, "score": 43.0, "pe_ratio": 16.1},
    {"ticker": "TGT", "name": "Target", "momentum": 52.1, "valuation": 42.8, "sentiment": 54.1, "score": 49.6, "pe_ratio": 18.7},
    {"ticker": "HD", "name": "The Home Depot", "momentum": 48.3, "valuation": 38.9, "sentiment": 51.2, "score": 46.1, "pe_ratio": 22.3},
    {"ticker": "LOWE", "name": "Lowe's", "momentum": 45.7, "valuation": 35.2, "sentiment": 49.8, "score": 43.5, "pe_ratio": 19.8},
    {"ticker": "NKE", "name": "Nike", "momentum": 42.1, "valuation": 32.4, "sentiment": 52.3, "score": 42.2, "pe_ratio": 24.1},
    {"ticker": "ADBE", "name": "Adobe Systems", "momentum": 64.1, "valuation": 22.3, "sentiment": 56.8, "score": 47.7, "pe_ratio": 38.5},
    {"ticker": "NOW", "name": "ServiceNow", "momentum": 62.8, "valuation": 18.5, "sentiment": 55.4, "score": 45.6, "pe_ratio": 68.2},
    {"ticker": "SHOP", "name": "Shopify", "momentum": 59.3, "valuation": 22.1, "sentiment": 57.8, "score": 46.4, "pe_ratio": 45.3},
    {"ticker": "SPOT", "name": "Spotify", "momentum": 68.5, "valuation": 28.9, "sentiment": 59.1, "score": 52.1, "pe_ratio": 62.1},
    {"ticker": "TWTR", "name": "Twitter", "momentum": 31.2, "valuation": 15.3, "sentiment": 38.7, "score": 28.4, "pe_ratio": 8.5},
    {"ticker": "SNAP", "name": "Snap Inc.", "momentum": 45.2, "valuation": 12.8, "sentiment": 42.3, "score": 33.4, "pe_ratio": 35.2},
    {"ticker": "PINS", "name": "Pinterest", "momentum": 38.9, "valuation": 18.4, "sentiment": 45.6, "score": 34.3, "pe_ratio": 28.9},
    {"ticker": "ROKU", "name": "Roku", "momentum": 52.1, "valuation": 14.2, "sentiment": 48.9, "score": 38.3, "pe_ratio": 35.4},
    {"ticker": "COIN", "name": "Coinbase", "momentum": 71.3, "valuation": 11.2, "sentiment": 52.8, "score": 45.1, "pe_ratio": 98.3},
    {"ticker": "ASML", "name": "ASML Holding", "momentum": 75.2, "valuation": 32.1, "sentiment": 61.4, "score": 56.2, "pe_ratio": 43.2},
]


def get_news_for_ticker(ticker):
    """Fetch real news from NewsAPI for a stock ticker"""
    try:
        url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])[:4]
            headlines = [
                {"title": article['title'], "url": article['url'], "source": article.get('source', {}).get('name', 'News')}
                for article in articles
            ]
            return headlines
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")
    return []


@app.route('/')
def home():
    return render_template('dashboard.html')


@app.route('/health')
def health():
    return jsonify({"status": "ok"})


@app.route('/api/stocks')
def stocks():
    return jsonify(STOCKS)


@app.route('/api/news/<ticker>')
def news(ticker):
    headlines = get_news_for_ticker(ticker)
    return jsonify({"ticker": ticker, "headlines": headlines})


@app.route('/api/refresh')
def refresh():
    return jsonify({"success": True, "stocks": STOCKS})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
