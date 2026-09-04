"""
Web dashboard for stock screener results.
Run: python web_app.py
Then visit http://localhost:5000
"""
from flask import Flask, render_template, jsonify
from datetime import date
import os
import json

app = Flask(__name__, template_folder='templates')

# Mock data - fallback when dependencies aren't available
MOCK_STOCKS = [
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


def load_csv_data():
    """Try to load data from CSV, return mock data if unavailable."""
    try:
        import pandas as pd
        results_file = f"daily_scores_{date.today().isoformat()}.csv"
        if os.path.exists(results_file):
            df = pd.read_csv(results_file)
            stocks = []
            for _, row in df.iterrows():
                stocks.append({
                    "ticker": str(row.get('ticker', 'N/A')),
                    "name": str(row.get('name', 'N/A')),
                    "momentum": float(row.get('momentum', 50)),
                    "valuation": float(row.get('valuation', 50)),
                    "sentiment": float(row.get('sentiment', 50)),
                    "score": float(row.get('score', 50)),
                    "pe_ratio": float(row['pe_ratio']) if pd.notna(row.get('pe_ratio')) else None,
                    "headlines_used": int(row.get('headlines_used', 0))
                })
            return stocks
    except Exception as e:
        print(f"Could not load CSV: {e}")

    return MOCK_STOCKS


@app.route('/')
def dashboard():
    """Main dashboard page."""
    try:
        return render_template('dashboard.html')
    except Exception as e:
        print(f"Dashboard error: {e}")
        return f"<h1>Stock Tracker</h1><p>Dashboard loading...</p>", 500


@app.route('/health')
def health():
    """Health check endpoint for Railway."""
    return jsonify({"status": "ok", "service": "stock-tracker"}), 200


@app.route('/api/stocks')
def api_stocks():
    """API endpoint returning stock data as JSON."""
    try:
        stocks = load_csv_data()
        return jsonify(stocks), 200
    except Exception as e:
        print(f"API error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/refresh')
def refresh_data():
    """Refresh stock data by running screener."""
    try:
        # Try to import and run screener
        try:
            from main import run as run_screener
            df = run_screener()

            if df.empty:
                stocks = MOCK_STOCKS
            else:
                stocks = []
                for _, row in df.iterrows():
                    stocks.append({
                        "ticker": str(row.get('ticker', 'N/A')),
                        "name": str(row.get('name', 'N/A')),
                        "momentum": float(row.get('momentum', 50)),
                        "valuation": float(row.get('valuation', 50)),
                        "sentiment": float(row.get('sentiment', 50)),
                        "score": float(row.get('score', 50)),
                        "pe_ratio": float(row['pe_ratio']) if pd.notna(row.get('pe_ratio')) else None,
                        "headlines_used": int(row.get('headlines_used', 0))
                    })
        except ImportError:
            print("Could not import main.py, using mock data")
            stocks = MOCK_STOCKS

        return jsonify({"success": True, "stocks": stocks}), 200
    except Exception as e:
        print(f"Refresh error: {e}")
        return jsonify({"success": False, "stocks": MOCK_STOCKS, "message": str(e)}), 200


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    print("Starting Stock Tracker Dashboard...")
    print(f"Visit http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
