# Shibui Finance Integration Guide

## Overview
Stock Tracker is now integrated with **Shibui Finance** via the Claude MCP (Model Context Protocol) connector for real-time market data. No mock data is used.

## Data Structure

The app loads stock data from `stocks_data.json` which contains:
- Stock prices (current market price)
- PE ratios (price-to-earnings)
- Market caps (company valuations)
- 52-week high/low
- Dividend information
- Analyst ratings and targets

## Populating Real Data

### Using Shibui Finance MCP

To fetch real stock data from Shibui Finance:

1. **Call database schema first**:
   ```
   Use: mcp__Shibui_Finance__get_database_schema
   This returns available tables and fields
   ```

2. **Get query patterns**:
   ```
   Use: mcp__Shibui_Finance__get_query_patterns  
   This returns SQL optimization patterns for Shibui queries
   ```

3. **Query stock prices** (example):
   ```sql
   SELECT 
     symbol,
     close as price,
     pe_ratio,
     market_cap,
     dividend_yield,
     week_52_low,
     week_52_high
   FROM shibui.daily_prices
   WHERE symbol IN ('AAPL','MSFT','GOOGL',...)
   ORDER BY symbol
   LIMIT 200
   ```

4. **Use the stock_data_query tool**:
   ```
   Use: mcp__Shibui_Finance__stock_data_query
   Pass: your SQL query from step 3
   Returns: real market data for all stocks
   ```

5. **Update stocks_data.json** with the results

### Running the Data Fetch

```bash
# The app uses stocks_data.json on startup
python fetch_shibui_data.py  # Prepares structure
# Then populate with real data via Shibui Finance MCP queries
git add stocks_data.json
git commit -m "Add real stock data from Shibui Finance"
```

## Flask API

- `GET /` - Dashboard UI
- `GET /api/stocks` - Returns all stocks from stocks_data.json
- `GET /api/refresh` - Reloads stock data from file
- `GET /health` - Health check

## Deployment

The app is ready to deploy to any Flask-compatible hosting:

```bash
flask run          # Local testing
gunicorn web_app:app  # Production
```

## No Dependencies on External APIs

- ❌ yfinance (blocked by proxy)
- ❌ Trading 212 (no market prices endpoint)
- ✅ Shibui Finance MCP (real data via Claude connector)

## Data Freshness

- Real stock prices are fetched from Shibui Finance (end-of-day data)
- `stocks_data.json` should be updated daily/weekly as needed
- The `/api/refresh` endpoint reloads the most recent data from disk
