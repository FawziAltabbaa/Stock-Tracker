"""
Web dashboard for stock screener results.
Run: python web_app.py
Then visit http://localhost:5000
"""
from flask import Flask, render_template, jsonify
from datetime import date
import pandas as pd
import os
import sys

app = Flask(__name__, template_folder='templates')

def get_results():
    """Load or generate stock scores."""
    try:
        results_file = f"daily_scores_{date.today().isoformat()}.csv"
        if os.path.exists(results_file):
            return pd.read_csv(results_file)
    except Exception as e:
        print(f"Error loading CSV: {e}")

    # Try to run screener as fallback
    try:
        print("Running screener to generate initial data...")
        from main import run as run_screener
        return run_screener()
    except Exception as e:
        print(f"Error running screener: {e}")
        # Return empty dataframe with correct structure
        return pd.DataFrame(columns=['ticker', 'name', 'momentum', 'valuation', 'sentiment', 'score', 'pe_ratio', 'headlines_used'])


@app.route('/')
def dashboard():
    """Main dashboard page."""
    try:
        return render_template('dashboard.html')
    except Exception as e:
        print(f"Dashboard error: {e}")
        return f"<h1>Stock Tracker</h1><p>Dashboard loading...</p><p>Error: {e}</p>", 500


@app.route('/health')
def health():
    """Health check endpoint for Railway."""
    return jsonify({"status": "ok", "service": "stock-tracker"}), 200


@app.route('/api/stocks')
def api_stocks():
    """API endpoint returning stock data as JSON."""
    try:
        df = get_results()
        if df.empty:
            return jsonify([]), 200

        stocks = []
        for _, row in df.iterrows():
            try:
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
            except Exception as e:
                print(f"Error processing row: {e}")
                continue

        return jsonify(stocks), 200
    except Exception as e:
        print(f"API error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/refresh')
def refresh_data():
    """Refresh stock data by running screener."""
    try:
        print("Refreshing stock data...")
        from main import run as run_screener
        df = run_screener()

        if df.empty:
            return jsonify({"success": False, "stocks": [], "message": "No data available"}), 200

        stocks = []
        for _, row in df.iterrows():
            try:
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
            except Exception as e:
                print(f"Error processing row: {e}")
                continue

        return jsonify({"success": True, "stocks": stocks}), 200
    except Exception as e:
        print(f"Refresh error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    print("Starting Stock Tracker Dashboard...")
    print(f"Visit http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
