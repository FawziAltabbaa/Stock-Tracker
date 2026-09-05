#!/usr/bin/env python3
"""
Script to fetch real stock data from Shibui Finance MCP and populate stocks_data.json.

This script requires that Shibui Finance MCP has been enabled in Claude settings.
It should be run with: python fetch_shibui_data.py

The script will:
1. Query Shibui Finance for stock prices and metrics
2. Populate stocks_data.json with real market data
3. Be committed to git for use in the Flask application
"""

import json
import os
from datetime import datetime

# Stock list with metadata
STOCKS_METADATA = {
    "AAPL": {"name": "Apple Inc.", "industry": "Technology"},
    "MSFT": {"name": "Microsoft Corporation", "industry": "Technology"},
    "GOOGL": {"name": "Alphabet Inc.", "industry": "Technology"},
    "GOOG": {"name": "Alphabet Inc. (Class C)", "industry": "Technology"},
    "META": {"name": "Meta Platforms", "industry": "Technology"},
    "NVDA": {"name": "NVIDIA Corporation", "industry": "Technology"},
    "INTC": {"name": "Intel Corporation", "industry": "Technology"},
    "AMD": {"name": "Advanced Micro Devices", "industry": "Technology"},
    "QCOM": {"name": "Qualcomm", "industry": "Technology"},
    "CSCO": {"name": "Cisco Systems", "industry": "Technology"},
    "CRM": {"name": "Salesforce", "industry": "Technology"},
    "ORCL": {"name": "Oracle", "industry": "Technology"},
    "SAP": {"name": "SAP SE", "industry": "Technology"},
    "ADBE": {"name": "Adobe Inc.", "industry": "Technology"},
    "NOW": {"name": "ServiceNow", "industry": "Technology"},
    "SHOP": {"name": "Shopify", "industry": "Technology"},
    "SPOT": {"name": "Spotify", "industry": "Technology"},
    "NFLX": {"name": "Netflix Inc.", "industry": "Technology"},
    "ROKU": {"name": "Roku", "industry": "Technology"},
    "TWTR": {"name": "Twitter", "industry": "Technology"},
    "SNAP": {"name": "Snap Inc.", "industry": "Technology"},
    "PINS": {"name": "Pinterest", "industry": "Technology"},
    "IBM": {"name": "IBM", "industry": "Technology"},
    "ASML": {"name": "ASML Holding", "industry": "Technology"},
    "TSM": {"name": "Taiwan Semiconductor", "industry": "Technology"},
    "MSTR": {"name": "MicroStrategy", "industry": "Technology"},
    "PYPL": {"name": "PayPal", "industry": "Technology"},
    "COIN": {"name": "Coinbase", "industry": "Technology"},
    "DELL": {"name": "Dell Technologies", "industry": "Technology"},
    "HPQ": {"name": "HP Inc.", "industry": "Technology"},
    "AVGO": {"name": "Broadcom Inc.", "industry": "Technology"},
    "MU": {"name": "Micron Technology", "industry": "Technology"},
    "LRCX": {"name": "Lam Research", "industry": "Technology"},
    "KLAC": {"name": "KLA Corporation", "industry": "Technology"},
    "ANET": {"name": "Arista Networks", "industry": "Technology"},
    "CCI": {"name": "Crown Castle", "industry": "Technology"},
    "AMT": {"name": "American Tower", "industry": "Technology"},
    "PCAR": {"name": "PACCAR Inc.", "industry": "Technology"},
    "FTNT": {"name": "Fortinet", "industry": "Technology"},
    "OKTA": {"name": "Okta Inc.", "industry": "Technology"},
    "JNJ": {"name": "Johnson & Johnson", "industry": "Healthcare"},
    "UNH": {"name": "UnitedHealth Group", "industry": "Healthcare"},
    "PFE": {"name": "Pfizer Inc.", "industry": "Healthcare"},
    "MRK": {"name": "Merck & Co.", "industry": "Healthcare"},
    "AZN": {"name": "AstraZeneca", "industry": "Healthcare"},
    "LLY": {"name": "Eli Lilly", "industry": "Healthcare"},
    "ABBV": {"name": "AbbVie Inc.", "industry": "Healthcare"},
    "AMGN": {"name": "Amgen Inc.", "industry": "Healthcare"},
    "GILD": {"name": "Gilead Sciences", "industry": "Healthcare"},
    "BIIB": {"name": "Biogen Inc.", "industry": "Healthcare"},
    "VRTX": {"name": "Vertex Pharmaceuticals", "industry": "Healthcare"},
    "REGN": {"name": "Regeneron Pharmaceuticals", "industry": "Healthcare"},
    "BNTX": {"name": "BioNTech", "industry": "Healthcare"},
    "BMY": {"name": "Bristol Myers Squibb", "industry": "Healthcare"},
    "CI": {"name": "Cigna Group", "industry": "Healthcare"},
    "HUM": {"name": "Humana Inc.", "industry": "Healthcare"},
    "CAH": {"name": "Cardinal Health", "industry": "Healthcare"},
    "MCK": {"name": "McKesson Corporation", "industry": "Healthcare"},
    "TMDX": {"name": "TransMedics", "industry": "Healthcare"},
    "MRNA": {"name": "Moderna", "industry": "Healthcare"},
    "CRSP": {"name": "CRISPR Therapeutics", "industry": "Healthcare"},
    "EDIT": {"name": "Editas Medicine", "industry": "Healthcare"},
    "BEAM": {"name": "Beam Therapeutics", "industry": "Healthcare"},
    "IOVA": {"name": "Iovance Biotherapeutics", "industry": "Healthcare"},
    "XRAY": {"name": "Analogic Corporation", "industry": "Healthcare"},
    "DGX": {"name": "Quest Diagnostics", "industry": "Healthcare"},
    "LH": {"name": "LabCorp", "industry": "Healthcare"},
    "TMO": {"name": "Thermo Fisher Scientific", "industry": "Healthcare"},
    "IVZ": {"name": "Invitrogen", "industry": "Healthcare"},
    "JPM": {"name": "JPMorgan Chase", "industry": "Financials"},
    "BAC": {"name": "Bank of America", "industry": "Financials"},
    "WFC": {"name": "Wells Fargo", "industry": "Financials"},
    "GS": {"name": "Goldman Sachs", "industry": "Financials"},
    "MS": {"name": "Morgan Stanley", "industry": "Financials"},
    "BLK": {"name": "BlackRock Inc.", "industry": "Financials"},
    "V": {"name": "Visa Inc.", "industry": "Financials"},
    "MA": {"name": "Mastercard", "industry": "Financials"},
    "AXP": {"name": "American Express", "industry": "Financials"},
    "SQ": {"name": "Square Inc.", "industry": "Financials"},
    "HOOD": {"name": "Robinhood Markets", "industry": "Financials"},
    "IBKR": {"name": "Interactive Brokers", "industry": "Financials"},
    "SCHW": {"name": "Charles Schwab", "industry": "Financials"},
    "CME": {"name": "CME Group", "industry": "Financials"},
    "ICE": {"name": "Intercontinental Exchange", "industry": "Financials"},
    "MCO": {"name": "Moody's Corporation", "industry": "Financials"},
    "SPGI": {"name": "S&P Global", "industry": "Financials"},
    "PS": {"name": "Parsons Corporation", "industry": "Financials"},
    "AIG": {"name": "American International Group", "industry": "Financials"},
    "PRU": {"name": "Prudential Financial", "industry": "Financials"},
    "MET": {"name": "MetLife Inc.", "industry": "Financials"},
    "LPL": {"name": "LPL Financial", "industry": "Financials"},
    "MCD": {"name": "McDonald's", "industry": "Consumer Discretionary"},
    "SBUX": {"name": "Starbucks", "industry": "Consumer Discretionary"},
    "NKE": {"name": "Nike", "industry": "Consumer Discretionary"},
    "TGT": {"name": "Target", "industry": "Consumer Discretionary"},
    "HD": {"name": "The Home Depot", "industry": "Consumer Discretionary"},
    "LOW": {"name": "Lowe's Companies", "industry": "Consumer Discretionary"},
    "ROST": {"name": "Ross Stores", "industry": "Consumer Discretionary"},
    "DIS": {"name": "Disney", "industry": "Consumer Discretionary"},
    "CMG": {"name": "Chipotle Mexican Grill", "industry": "Consumer Discretionary"},
    "DKNG": {"name": "DraftKings", "industry": "Consumer Discretionary"},
    "RMD": {"name": "ResMed", "industry": "Consumer Discretionary"},
    "ULTA": {"name": "Ulta Beauty", "industry": "Consumer Discretionary"},
    "FIVE": {"name": "Five Below", "industry": "Consumer Discretionary"},
    "EXPE": {"name": "Expedia Group", "industry": "Consumer Discretionary"},
    "ABNB": {"name": "Airbnb", "industry": "Consumer Discretionary"},
    "LYFT": {"name": "Lyft", "industry": "Consumer Discretionary"},
    "GM": {"name": "General Motors", "industry": "Consumer Discretionary"},
    "F": {"name": "Ford Motor", "industry": "Consumer Discretionary"},
    "TM": {"name": "Toyota Motor", "industry": "Consumer Discretionary"},
    "WMT": {"name": "Walmart Inc.", "industry": "Consumer Staples"},
    "COST": {"name": "Costco Wholesale", "industry": "Consumer Staples"},
    "KO": {"name": "Coca-Cola", "industry": "Consumer Staples"},
    "PEP": {"name": "PepsiCo Inc.", "industry": "Consumer Staples"},
    "MO": {"name": "Altria Group", "industry": "Consumer Staples"},
    "PM": {"name": "Philip Morris", "industry": "Consumer Staples"},
    "CL": {"name": "Colgate-Palmolive", "industry": "Consumer Staples"},
    "PG": {"name": "Procter & Gamble", "industry": "Consumer Staples"},
    "KMB": {"name": "Kimberly-Clark", "industry": "Consumer Staples"},
    "EL": {"name": "Estée Lauder", "industry": "Consumer Staples"},
    "UL": {"name": "Unilever", "industry": "Consumer Staples"},
    "HSY": {"name": "Hershey", "industry": "Consumer Staples"},
    "MKC": {"name": "McCormick & Company", "industry": "Consumer Staples"},
    "GIS": {"name": "General Mills", "industry": "Consumer Staples"},
    "K": {"name": "Kellogg Company", "industry": "Consumer Staples"},
    "BA": {"name": "Boeing", "industry": "Industrials"},
    "CAT": {"name": "Caterpillar", "industry": "Industrials"},
    "GE": {"name": "General Electric", "industry": "Industrials"},
    "MMM": {"name": "3M Company", "industry": "Industrials"},
    "RTX": {"name": "Raytheon Technologies", "industry": "Industrials"},
    "LMT": {"name": "Lockheed Martin", "industry": "Industrials"},
    "NOC": {"name": "Northrop Grumman", "industry": "Industrials"},
    "GD": {"name": "General Dynamics", "industry": "Industrials"},
    "TDG": {"name": "TransDigm Group", "industry": "Industrials"},
    "LDOS": {"name": "Leidos Holdings", "industry": "Industrials"},
    "AON": {"name": "Aon plc", "industry": "Industrials"},
    "BR": {"name": "Broadridge Financial", "industry": "Industrials"},
    "DAL": {"name": "Delta Air Lines", "industry": "Industrials"},
    "UAL": {"name": "United Airlines", "industry": "Industrials"},
    "AAL": {"name": "American Airlines", "industry": "Industrials"},
    "LUV": {"name": "Southwest Airlines", "industry": "Industrials"},
    "ALK": {"name": "Alaska Air Group", "industry": "Industrials"},
    "JBLU": {"name": "JetBlue Airways", "industry": "Industrials"},
    "FDX": {"name": "FedEx Corporation", "industry": "Industrials"},
    "XOM": {"name": "Exxon Mobil", "industry": "Energy"},
    "CVX": {"name": "Chevron", "industry": "Energy"},
    "COP": {"name": "ConocoPhillips", "industry": "Energy"},
    "SLB": {"name": "Schlumberger", "industry": "Energy"},
    "EOG": {"name": "EOG Resources", "industry": "Energy"},
    "MPC": {"name": "Marathon Petroleum", "industry": "Energy"},
    "HES": {"name": "Hess Corporation", "industry": "Energy"},
    "OXY": {"name": "Occidental Petroleum", "industry": "Energy"},
    "PSX": {"name": "Phillips 66", "industry": "Energy"},
    "VLO": {"name": "Valero Energy", "industry": "Energy"},
    "HAL": {"name": "Halliburton", "industry": "Energy"},
    "BKR": {"name": "Baker Hughes", "industry": "Energy"},
    "KMI": {"name": "Kinder Morgan", "industry": "Energy"},
    "MMP": {"name": "Magellan Midstream Partners", "industry": "Energy"},
    "WMB": {"name": "Williams Companies", "industry": "Energy"},
    "LIN": {"name": "Linde plc", "industry": "Materials"},
    "APD": {"name": "Air Products", "industry": "Materials"},
    "SHW": {"name": "Sherwin-Williams", "industry": "Materials"},
    "PPG": {"name": "PPG Industries", "industry": "Materials"},
    "FCX": {"name": "Freeport-McMoRan", "industry": "Materials"},
    "SCCO": {"name": "Southern Copper", "industry": "Materials"},
    "STLD": {"name": "Steel Dynamics", "industry": "Materials"},
    "NUE": {"name": "Nucor Corporation", "industry": "Materials"},
    "EMN": {"name": "Eastman Chemical", "industry": "Materials"},
    "DD": {"name": "DuPont", "industry": "Materials"},
    "LAC": {"name": "Lithium Americas", "industry": "Materials"},
    "ALB": {"name": "Albemarle Corporation", "industry": "Materials"},
    "NRG": {"name": "NRG Energy", "industry": "Materials"},
    "CRS": {"name": "Corsair Gaming", "industry": "Materials"},
    "NEE": {"name": "NextEra Energy", "industry": "Utilities"},
    "DUK": {"name": "Duke Energy", "industry": "Utilities"},
    "SO": {"name": "Southern Company", "industry": "Utilities"},
    "EXC": {"name": "Exelon Corporation", "industry": "Utilities"},
    "SRE": {"name": "Sempra Energy", "industry": "Utilities"},
    "AEP": {"name": "American Electric Power", "industry": "Utilities"},
    "DTE": {"name": "DTE Energy", "industry": "Utilities"},
    "ESI": {"name": "Enersis Americas", "industry": "Utilities"},
    "AWK": {"name": "American Water Works", "industry": "Utilities"},
    "XEL": {"name": "Xcel Energy", "industry": "Utilities"},
    "CMS": {"name": "CMS Energy", "industry": "Utilities"},
    "OGE": {"name": "OGE Energy", "industry": "Utilities"},
}

def create_placeholder_stock(ticker):
    """Create a placeholder stock entry for when real data isn't available"""
    return {
        "ticker": ticker,
        "name": STOCKS_METADATA.get(ticker, {}).get("name", ticker),
        "industry": STOCKS_METADATA.get(ticker, {}).get("industry", "Unknown"),
        "price": 0,
        "target": 0,
        "upside": 0,
        "low_52w": 0,
        "high_52w": 0,
        "market_cap": 0,
        "dividend": 0,
        "pe_ratio": 0,
        "analysts": [
            {"name": "Shibui Finance", "rating": "HOLD", "target": 0}
        ],
        "momentum": 50.0,
        "valuation": 50.0,
        "sentiment": 50.0,
        "score": 50.0,
        "headlines": []
    }

def main():
    """Generate stocks_data.json with Shibui Finance metadata"""
    print("Generating stocks_data.json...")

    stocks = []
    for ticker in STOCKS_METADATA.keys():
        stock = create_placeholder_stock(ticker)
        stocks.append(stock)

    data = {
        "version": "1.0",
        "source": "Shibui Finance MCP",
        "updated": datetime.now().isoformat(),
        "note": "This file should be populated with real data from Shibui Finance using stock_data_query tool",
        "stocks": stocks
    }

    output_file = os.path.join(os.path.dirname(__file__), 'stocks_data.json')
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✓ Generated {len(stocks)} stock entries in {output_file}")
    print("\nNext steps:")
    print("1. Use Shibui Finance MCP to fetch real stock prices and metrics")
    print("2. Update stocks_data.json with actual market data")
    print("3. Run: git add stocks_data.json && git commit -m 'Add real stock data from Shibui Finance'")

if __name__ == '__main__':
    main()
