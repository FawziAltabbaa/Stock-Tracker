"""
Web dashboard for stock screener results.
Run: python web_app.py
Then visit http://localhost:5000
"""
from flask import Flask, render_template, jsonify
from datetime import date
import pandas as pd
from main import run as run_screener

app = Flask(__name__)
RESULTS_FILE = f"daily_scores_{date.today().isoformat()}.csv"


def get_results():
    """Load or generate stock scores."""
    try:
        return pd.read_csv(RESULTS_FILE)
    except FileNotFoundError:
        print("Running screener to generate initial data...")
        return run_screener()


@app.route('/')
def dashboard():
    """Main dashboard page."""
    return render_template('dashboard.html')


@app.route('/api/stocks')
def api_stocks():
    """API endpoint returning stock data as JSON."""
    df = get_results()
    if df.empty:
        return jsonify({"error": "No data available"}), 404

    stocks = []
    for _, row in df.iterrows():
        stocks.append({
            "ticker": row['ticker'],
            "name": row['name'],
            "momentum": float(row['momentum']),
            "valuation": float(row['valuation']),
            "sentiment": float(row['sentiment']),
            "score": float(row['score']),
            "pe_ratio": float(row['pe_ratio']) if pd.notna(row['pe_ratio']) else None,
            "headlines_used": int(row['headlines_used'])
        })

    return jsonify(stocks)


@app.route('/api/refresh')
def refresh_data():
    """Refresh stock data by running screener."""
    print("Refreshing stock data...")
    df = run_screener()
    if df.empty:
        return jsonify({"error": "Failed to fetch data"}), 500

    stocks = []
    for _, row in df.iterrows():
        stocks.append({
            "ticker": row['ticker'],
            "name": row['name'],
            "momentum": float(row['momentum']),
            "valuation": float(row['valuation']),
            "sentiment": float(row['sentiment']),
            "score": float(row['score']),
            "pe_ratio": float(row['pe_ratio']) if pd.notna(row['pe_ratio']) else None,
            "headlines_used": int(row['headlines_used'])
        })

    return jsonify({"success": True, "stocks": stocks})


if __name__ == '__main__':
    print("Starting Stock Tracker Dashboard...")
    print("Visit http://localhost:5000")
    app.run(debug=True, port=5000)
