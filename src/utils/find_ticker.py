import os 
import sys 
sys.path.append('../../')

import requests

finnhub_api_key = os.getenv("FINNHUB_API_KEY")


def find_ticker_finnhub(company_name, finnhub_key):
    url = "https://finnhub.io/api/v1/search"
    params = {
        "q": company_name,
        "token": finnhub_key
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    results = resp.json().get("result", [])

    company_name_lower = company_name.lower()
    
    for item in results:
        description = item.get("description", "").lower()
        if company_name_lower == description:
            return item.get("symbol")
    
    for item in results:
        description = item.get("description", "").lower()
        if company_name_lower in description:
            return item.get("symbol")
    
    if results:
        return results[0].get("symbol")
    
    return None
