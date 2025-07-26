import os 
import sys 
import requests 
import json 

sys.path.append("../../")


def get_company_overview(ticker, api_key):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "OVERVIEW",
        "symbol": ticker,
        "apikey": api_key
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data
 