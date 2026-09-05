import os
import json
from flask import Flask, render_template, jsonify
import logging

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
