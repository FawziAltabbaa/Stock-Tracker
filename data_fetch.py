"""
Pulls price history, fundamentals, and news headlines for a ticker.
Uses yfinance -- free, no API key required.
"""
import yfinance as yf
import pandas as pd


def get_price_history(ticker: str, period="3mo") -> pd.DataFrame:
    """Daily OHLCV history for momentum calculations."""
    hist = yf.Ticker(ticker).history(period=period)
    return hist


def get_fundamentals(ticker: str) -> dict:
    """Key valuation stats. Missing fields default to None."""
    info = yf.Ticker(ticker).info
    return {
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "peg_ratio": info.get("pegRatio"),
        "market_cap": info.get("marketCap"),
        "sector": info.get("sector"),
        "name": info.get("shortName", ticker),
    }


def get_news_headlines(ticker: str, limit: int = 8) -> list[str]:
    """Recent headlines for sentiment scoring."""
    try:
        news = yf.Ticker(ticker).news or []
    except Exception:
        news = []
    headlines = []
    for item in news[:limit]:
        title = item.get("content", {}).get("title") or item.get("title")
        if title:
            headlines.append(title)
    return headlines
