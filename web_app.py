import os
from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='templates')

STOCKS = [
    {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "momentum": 82.5,
        "valuation": 28.8,
        "sentiment": 60.8,
        "score": 58.8,
        "pe_ratio": 28.5,
        "headlines_used": 4
    },
    {
        "ticker": "NVDA",
        "name": "NVIDIA Corporation",
        "momentum": 84.0,
        "valuation": 0.0,
        "sentiment": 49.7,
        "score": 46.8,
        "pe_ratio": 52.4,
        "headlines_used": 4
    },
    {
        "ticker": "AMZN",
        "name": "Amazon.com Inc.",
        "momentum": 69.4,
        "valuation": 0.0,
        "sentiment": 63.1,
        "score": 46.4,
        "pe_ratio": 42.6,
        "headlines_used": 4
    },
    {
        "ticker": "MSFT",
        "name": "Microsoft Corporation",
        "momentum": 32.5,
        "valuation": 19.7,
        "sentiment": 58.9,
        "score": 37.9,
        "pe_ratio": 32.1,
        "headlines_used": 4
    },
    {
        "ticker": "TSLA",
        "name": "Tesla Inc.",
        "momentum": 42.0,
        "valuation": 0.0,
        "sentiment": 46.3,
        "score": 30.9,
        "pe_ratio": 65.3,
        "headlines_used": 4
    }
]


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
    return jsonify({"success": True, "stocks": STOCKS})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
