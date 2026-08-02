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

    from src.load.minio_loader import MinIOLoader
    minio_endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    minio_user = os.getenv("MINIO_ROOT_USER", "minioadmin")
    minio_password = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin123")
    bucket_name = "crypto-raw-data"
    
    extractor = CoinGeckoExtractor()
    coins = extractor.get_top_coins(limit=50)
    logger.info(f"Extracted {len(coins)} coins")

    loader = MinIOLoader(
        endpoint=minio_endpoint,
        access_key=minio_user,
        secret_key=minio_password,
        secure=False
    )

    raw_object_name = loader.save_json_to_raw(
        bucket_name=bucket_name,
        data=coins,
        prefix="coingecko"
    )

    logger.info(f"Raw data saved: {raw_object_name}")
    
    from src.transform.cleaner import DataCleaner
    cleaner = DataCleaner()
    cleaned_df = cleaner.clean_coins_data(coins)
    logger.info(f"Data cleaned: {len(cleaned_df)} rows")

    silver_object_name = loader.save_parquet_to_silver(
        bucket_name=bucket_name,
        df=cleaned_df,
        prefix="coingecko"
    )

    logger.info(f"Silver data saved: {silver_object_name}")
    
    logger.info("Pipeline completed successfully!")

if __name__ == "__main__":
    main()