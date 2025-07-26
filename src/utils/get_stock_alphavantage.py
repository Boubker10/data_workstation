import os 
import sys 
sys.path.append("../../")
import requests 
import json

alpha_api_key = os.getenv("ALPHA_API_KEY")

def get_stock_quote_alphavantage(ticker, api_key):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": ticker,
        "apikey": api_key
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    quote = data.get("Global Quote", {})
    return {
        "ticker": quote.get("01. symbol"),
        "open": quote.get("02. open"),
        "high": quote.get("03. high"),
        "low": quote.get("04. low"),
        "price": quote.get("05. price"),
        "volume": quote.get("06. volume"),
        "latest_trading_day": quote.get("07. latest trading day"),
        "previous_close": quote.get("08. previous close"),
        "change": quote.get("09. change"),
        "change_percent": quote.get("10. change percent")
    }
