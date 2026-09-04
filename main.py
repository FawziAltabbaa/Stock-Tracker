"""
Daily stock screener prototype.
Run: python main.py

Pulls each ticker in config.WATCHLIST, scores it on momentum,
valuation, and news sentiment, and prints a ranked table.

IMPORTANT: This produces informational scores, not financial advice.
Under UK FCA rules, personalised buy/sell recommendations are a
regulated activity. Keep any public-facing version framed as
analytics/information, not advice.
"""
from datetime import date
import pandas as pd

from config import WATCHLIST, WEIGHTS, NEWS_HEADLINES_PER_STOCK
from data_fetch import get_price_history, get_fundamentals, get_news_headlines
from scoring import score_momentum, score_valuation, score_sentiment, composite_score


def analyse_ticker(ticker: str) -> dict:
    hist = get_price_history(ticker)
    fundamentals = get_fundamentals(ticker)
    headlines = get_news_headlines(ticker, NEWS_HEADLINES_PER_STOCK)

    m = score_momentum(hist)
    v = score_valuation(fundamentals)
    s = score_sentiment(headlines)
    composite = composite_score(m, v, s, WEIGHTS)

    return {
        "ticker": ticker,
        "name": fundamentals.get("name"),
        "momentum": round(m, 1),
        "valuation": round(v, 1),
        "sentiment": round(s, 1),
        "score": composite,
        "pe_ratio": fundamentals.get("pe_ratio"),
        "headlines_used": len(headlines),
    }


def run():
    print(f"Fetching data for {len(WATCHLIST)} tickers...\n")
    results = []
    for ticker in WATCHLIST:
        try:
            results.append(analyse_ticker(ticker))
            print(f"  done: {ticker}")
        except Exception as e:
            print(f"  failed: {ticker} ({e})")

    if not results:
        print("\nNo data retrieved -- check your internet connection.")
        return pd.DataFrame()

    df = pd.DataFrame(results).sort_values("score", ascending=False).reset_index(drop=True)

    print("\n=== Daily Ranking ===")
    print(df.to_string(index=False))

    out_path = f"daily_scores_{date.today().isoformat()}.csv"
    df.to_csv(out_path, index=False)
    print(f"\nSaved to {out_path}")
    print("\nNote: informational scores only, not financial advice.")
    return df


if __name__ == "__main__":
    run()
