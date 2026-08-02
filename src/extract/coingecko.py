import requests
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class CoinGeckoExtractor:

    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self, api_key: str = None):

        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"x-cg-demo-api-key": api_key})
        
        logger.info("CoinGeckoExtractor initialized")

    
    def get_top_coins(self, vs_currency: str = "usd", limit: int = 10) -> List[Dict[str, Any]]:
        
        endpoint = f"{self.BASE_URL}/coins/markets"
        params = {
            "vs_currency": vs_currency,
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": False
        }
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully fetched {len(data)} coins")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise