from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.utils.logger import setup_logging
import logging
from src.extract.coingecko import CoinGeckoExtractor

logger = logging.getLogger(__name__)


def main():

    setup_logging()
    logger.info("Starting crypto data extraction...")
    
    extractor = CoinGeckoExtractor()
    coins = extractor.get_top_coins(limit=5)
    
    logger.info(f"Fetched {len(coins)} coins")
    for coin in coins[:3]:
        logger.info(f"  - {coin['name']} ({coin['symbol'].upper()}): ${coin['current_price']}")


if __name__ == "__main__":
    main()