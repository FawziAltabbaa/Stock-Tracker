# --- User settings ---

# Tickers the user wants tracked (edit this list freely)
WATCHLIST = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]

# How much each factor counts toward the final score (must sum to 1.0)
WEIGHTS = {
    "momentum": 0.35,   # price trend (20d vs 50d moving average, recent % change)
    "valuation": 0.30,  # P/E relative to a sane benchmark
    "sentiment": 0.35,  # recent news sentiment
}

# How many recent news headlines to analyse per stock
NEWS_HEADLINES_PER_STOCK = 8
