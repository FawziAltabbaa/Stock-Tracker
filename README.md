# Stock Screener Prototype

Free, no API keys needed. Scores your watchlist daily on:
- **Momentum** — price vs 20/50-day moving averages, 1-month trend
- **Valuation** — P/E ratio vs a benchmark
- **Sentiment** — VADER sentiment on recent news headlines

## Setup
```
pip install yfinance vaderSentiment pandas
```

## Run
```
python main.py
```
Edit `config.py` to change your watchlist or the weighting between factors.

Outputs a ranked table in the terminal and saves `daily_scores_YYYY-MM-DD.csv`.

## Important
- This produces **informational scores**, not financial advice. In the UK, giving
  personalised buy/sell recommendations is a regulated FCA activity — keep any
  public-facing version framed as analytics, not advice.
- I couldn't test-run this in Claude's sandbox because it can't reach Yahoo
  Finance (network allowlist). Run it locally — it should work out of the box.

## Next steps (once this works for you)
1. **Dashboard**: wrap `main.py`'s output in Streamlit (`pip install streamlit`) — a few lines gets you a browser UI with a table and daily refresh button. Free to host on Streamlit Community Cloud.
2. **Automation**: schedule `main.py` to run daily (cron, or a free GitHub Actions workflow) and save results.
3. **Subscriptions**: once you have a working dashboard, Stripe + a simple user-tickers database (SQLite is fine to start) gets you to a real subscription product.
