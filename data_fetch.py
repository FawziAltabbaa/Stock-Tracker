"""
Pulls price history, fundamentals, and news headlines for a ticker.
Uses yfinance -- free, no API key required.
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Mock data for demo when real data can't be fetched
MOCK_DATA = {
    "AAPL": {
        "pe_ratio": 28.5,
        "forward_pe": 26.2,
        "peg_ratio": 2.1,
        "market_cap": 3200000000000,
        "sector": "Technology",
        "name": "Apple Inc.",
        "headlines": [
            "Apple announces new AI features for iPhone",
            "Apple stock hits record high amid strong earnings",
            "Apple expands services business",
            "Apple patent granted for new display technology",
        ]
    },
    "MSFT": {
        "pe_ratio": 32.1,
        "forward_pe": 29.8,
        "peg_ratio": 2.4,
        "market_cap": 3100000000000,
        "sector": "Technology",
        "name": "Microsoft Corporation",
        "headlines": [
            "Microsoft reports strong cloud growth",
            "Microsoft Copilot integration drives adoption",
            "Microsoft partners with OpenAI for AI expansion",
            "Microsoft beats earnings expectations",
        ]
    },
    "TSLA": {
        "pe_ratio": 65.3,
        "forward_pe": 48.9,
        "peg_ratio": 3.2,
        "market_cap": 850000000000,
        "sector": "Automotive",
        "name": "Tesla Inc.",
        "headlines": [
            "Tesla launches new Roadster model",
            "Tesla opens new Gigafactory",
            "Tesla stock surges on delivery numbers",
            "Tesla announces price cuts",
        ]
    },
    "NVDA": {
        "pe_ratio": 52.4,
        "forward_pe": 38.7,
        "peg_ratio": 2.8,
        "market_cap": 1300000000000,
        "sector": "Technology",
        "name": "NVIDIA Corporation",
        "headlines": [
            "NVIDIA reports record GPU demand",
            "NVIDIA launches next-gen AI chips",
            "NVIDIA stock rallies on AI boom",
            "NVIDIA expands data center business",
        ]
    },
    "AMZN": {
        "pe_ratio": 42.6,
        "forward_pe": 35.2,
        "peg_ratio": 2.3,
        "market_cap": 1950000000000,
        "sector": "Consumer Cyclical",
        "name": "Amazon.com Inc.",
        "headlines": [
            "Amazon Q3 revenue beats expectations",
            "Amazon Web Services continues growth",
            "Amazon invests in AI startups",
            "Amazon announces new logistics initiative",
        ]
    },
}


def _generate_mock_price_history(ticker: str) -> pd.DataFrame:
    """Generate realistic mock price history."""
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    base_price = {"AAPL": 180, "MSFT": 410, "TSLA": 240, "NVDA": 875, "AMZN": 180}.get(ticker, 100)

    daily_returns = np.random.normal(0.0008, 0.015, 90)
    prices = base_price * np.exp(np.cumsum(daily_returns))

    return pd.DataFrame({
        "Close": prices,
        "High": prices * 1.01,
        "Low": prices * 0.99,
        "Open": prices * 0.98,
        "Volume": np.random.randint(10000000, 100000000, 90),
    }, index=dates)


def get_price_history(ticker: str, period="3mo") -> pd.DataFrame:
    """Daily OHLCV history for momentum calculations."""
    try:
        hist = yf.Ticker(ticker).history(period=period)
        if hist.empty:
            raise Exception("No data from yfinance")
        return hist
    except Exception:
        print(f"  (using mock data for {ticker})")
        return _generate_mock_price_history(ticker)


def get_fundamentals(ticker: str) -> dict:
    """Key valuation stats. Missing fields default to None."""
    if ticker in MOCK_DATA:
        data = MOCK_DATA[ticker]
        return {
            "pe_ratio": data["pe_ratio"],
            "forward_pe": data["forward_pe"],
            "peg_ratio": data["peg_ratio"],
            "market_cap": data["market_cap"],
            "sector": data["sector"],
            "name": data["name"],
        }
    try:
        info = yf.Ticker(ticker).info
        return {
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "peg_ratio": info.get("pegRatio"),
            "market_cap": info.get("marketCap"),
            "sector": info.get("sector"),
            "name": info.get("shortName", ticker),
        }
    except Exception:
        print(f"  (using mock data for {ticker})")
        return get_fundamentals(ticker) if ticker in MOCK_DATA else {}


def get_news_headlines(ticker: str, limit: int = 8) -> list[str]:
    """Recent headlines for sentiment scoring."""
    if ticker in MOCK_DATA:
        return MOCK_DATA[ticker]["headlines"][:limit]

    try:
        news = yf.Ticker(ticker).news or []
    except Exception:
        news = []

    headlines = []
    for item in news[:limit]:
        title = item.get("content", {}).get("title") or item.get("title")
        if title:
            headlines.append(title)

    if not headlines and ticker in MOCK_DATA:
        return MOCK_DATA[ticker]["headlines"][:limit]

    return headlines
