"""
Turns raw data into a 0-100 score per factor, then a weighted composite.
Simple, explainable rules -- no black box.
"""
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()


def score_momentum(hist: pd.DataFrame) -> float:
    """0-100. Rewards price above its moving averages and positive recent trend."""
    if hist is None or hist.empty or len(hist) < 20:
        return 50.0  # neutral if not enough data

    close = hist["Close"]
    ma20 = close.rolling(20).mean().iloc[-1]
    ma50 = close.rolling(min(50, len(close))).mean().iloc[-1]
    latest = close.iloc[-1]
    pct_change_1m = (latest / close.iloc[-21] - 1) * 100 if len(close) > 21 else 0

    score = 50.0
    if latest > ma20:
        score += 15
    if latest > ma50:
        score += 15
    score += max(min(pct_change_1m, 20), -20)  # cap influence at +-20 pts
    return max(0, min(100, score))


def score_valuation(fundamentals: dict) -> float:
    """0-100. Lower P/E relative to a rough 'fair' benchmark of 20 scores higher.
    This is a simple heuristic, not a sector-adjusted model."""
    pe = fundamentals.get("pe_ratio")
    if pe is None or pe <= 0:
        return 50.0

    benchmark = 20.0
    if pe <= benchmark:
        score = 50 + (benchmark - pe) / benchmark * 50
    else:
        score = 50 - (pe - benchmark) / benchmark * 50
    return max(0, min(100, score))


def score_sentiment(headlines: list[str]) -> float:
    """0-100. Average VADER compound sentiment across headlines, rescaled."""
    if not headlines:
        return 50.0
    compounds = [_analyzer.polarity_scores(h)["compound"] for h in headlines]
    avg = sum(compounds) / len(compounds)  # ranges -1 to 1
    return (avg + 1) / 2 * 100


def composite_score(momentum: float, valuation: float, sentiment: float, weights: dict) -> float:
    return round(
        momentum * weights["momentum"]
        + valuation * weights["valuation"]
        + sentiment * weights["sentiment"],
        1,
    )
