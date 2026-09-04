# Stock Tracker Web Dashboard

A beautiful, interactive web interface for your stock screener.

## Quick Start

### 1. Install Dependencies
```bash
pip install flask pandas yfinance vaderSentiment
```

### 2. Run the Web App
```bash
python web_app.py
```

### 3. Open in Browser
Visit `http://localhost:5000` in your web browser

## Features

### 📊 Dashboard View
- **Live Stock Rankings** - Stocks sorted by composite score (highest first)
- **Momentum Score** - Price trend and technical analysis (0-100)
- **Valuation Score** - P/E ratio relative to benchmark (0-100)
- **Sentiment Score** - News headline sentiment analysis (0-100)

### 📈 Visual Indicators
- Color-coded scores (excellent/good/moderate/poor)
- Progress bars for visual comparison
- Performance metrics inline in table
- Responsive design for mobile and desktop

### 🔄 Interactive Controls
- **Refresh Data Button** - Re-run screener to get latest scores
- **Download CSV** - Export results for further analysis
- Live timestamp showing when data was last updated

### 📊 Summary Cards
- **Top Stock** - Highest scoring ticker
- **Avg Score** - Average composite score across all stocks
- **Total Stocks** - Number of stocks being tracked

## API Endpoints

### GET `/api/stocks`
Returns current stock data as JSON
```json
[
  {
    "ticker": "AAPL",
    "name": "Apple Inc.",
    "momentum": 82.5,
    "valuation": 28.8,
    "sentiment": 60.8,
    "score": 58.8,
    "pe_ratio": 28.5,
    "headlines_used": 4
  }
]
```

### GET `/api/refresh`
Runs the screener and returns updated stock data
```json
{
  "success": true,
  "stocks": [...]
}
```

## Customization

### Change Watched Stocks
Edit `config.py` and modify the `WATCHLIST`:
```python
WATCHLIST = ["AAPL", "MSFT", "GOOGL", "AMZN"]
```

### Adjust Scoring Weights
Edit `config.py` to change factor weights:
```python
WEIGHTS = {
    "momentum": 0.35,    # Price trend
    "valuation": 0.30,   # P/E ratio
    "sentiment": 0.35,   # News sentiment
}
```

### Change News Sources
Edit `config.py` to adjust headlines per stock:
```python
NEWS_HEADLINES_PER_STOCK = 10  # Fetch 10 headlines instead of 8
```

## Understanding Scores

### Momentum (0-100)
- Rewards prices above 20-day and 50-day moving averages
- Factors in 1-month percentage change
- Higher = stronger uptrend

### Valuation (0-100)
- Compares P/E ratio to 20 (a "fair" benchmark)
- Higher = lower P/E (undervalued)
- Lower P/E means stronger value score

### Sentiment (0-100)
- Analyzes recent news headlines using VADER sentiment analysis
- Higher = more positive news
- Ranges from -1 (very negative) to 1 (very positive)

### Composite Score
Weighted average: `(momentum × 0.35) + (valuation × 0.30) + (sentiment × 0.35)`

## Data Storage

Results are automatically saved to CSV files:
- Format: `daily_scores_YYYY-MM-DD.csv`
- Location: Project root directory
- Contains all scores and metrics for archival

## Troubleshooting

### Can't connect to web interface?
- Check that Flask is running: `ps aux | grep web_app.py`
- Try accessing `http://127.0.0.1:5000` instead of `localhost`
- Check firewall settings

### Data not loading?
- Ensure `main.py` runs successfully: `python main.py`
- Check internet connection for real data fetching
- Mock data will be used automatically if APIs are unavailable

### Refresh button not working?
- Check Flask server logs
- Ensure yfinance and dependencies are installed
- Verify network connectivity

## Deployment

### For Production
Replace Flask's development server with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

### On Cloud (e.g., Heroku)
1. Create `Procfile`:
   ```
   web: gunicorn web_app:app
   ```

2. Deploy with git push

## Future Enhancements

- Email/SMS alerts for score thresholds
- Historical trend charts
- Customizable watchlists per user
- Price target predictions
- Integration with trading platforms

## License

Informational scores only. Not financial advice.
