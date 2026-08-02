from pathlib import Path
import sys
import os
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.utils.logger import setup_logging
import logging
from src.extract.coingecko import CoinGeckoExtractor

load_dotenv()
logger = logging.getLogger(__name__)


def main():

    setup_logging()
    logger.info("Starting crypto data extraction...")
    
    extractor = CoinGeckoExtractor()
    coins = extractor.get_top_coins(limit=10)
    logger.info(f"Extracted {len(coins)} coins")

    from src.load.minio_loader import MinIOLoader
    minio_endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    minio_user = os.getenv("MINIO_ROOT_USER", "minioadmin")
    minio_password = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin123")

    loader = MinIOLoader(
        endpoint=minio_endpoint,
        access_key=minio_user,
        secret_key=minio_password,
        secure=False
    )

    
    loader.save_json_to_raw(
        bucket_name="crypto-raw-data",
        data=coins,
        prefix="coingecko"
    )

    logger.info("Pipeline completed successfully!")

if __name__ == "__main__":
    main()