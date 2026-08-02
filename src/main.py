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
from src.utils.config import AppConfig

load_dotenv()
logger = logging.getLogger(__name__)


def main():
    setup_logging()
    logger.info("Starting crypto data pipeline...")
    
    config = AppConfig()
    
    # 1. Extract
    from src.extract.coingecko import CoinGeckoExtractor
    extractor = CoinGeckoExtractor()
    coins = extractor.get_top_coins(limit=50)
    logger.info(f"Extracted {len(coins)} coins")
    
    # 2. Load to Raw (JSON) - MinIO
    from src.load.minio_loader import MinIOLoader
    minio_loader = MinIOLoader(
        endpoint=config.minio.endpoint,
        access_key=config.minio.access_key,
        secret_key=config.minio.secret_key,
        secure=False
    )
    
    raw_object_name = minio_loader.save_json_to_raw(
        bucket_name=config.minio.bucket_name,
        data=coins,
        prefix="coingecko"
    )
    logger.info(f"Raw data saved: {raw_object_name}")
    
    # 3. Transform (Clean)
    from src.transform.cleaner import DataCleaner
    cleaner = DataCleaner()
    cleaned_df = cleaner.clean_coins_data(coins)
    logger.info(f"Data cleaned: {len(cleaned_df)} rows")
    
    # 4. Load to Silver (Parquet) - MinIO
    silver_object_name = minio_loader.save_parquet_to_silver(
        bucket_name=config.minio.bucket_name,
        df=cleaned_df,
        prefix="coingecko"
    )
    logger.info(f"Silver data saved: {silver_object_name}")
    
    # 5. Load to Data Warehouse - PostgreSQL
    from src.load.postgres_loader import PostgresLoader
    pg_loader = PostgresLoader(config.postgres)
    
    pg_loader.upsert_coins(coins)
    
    pg_loader.load_daily_prices(cleaned_df)
    
    logger.info("Pipeline completed successfully!")


if __name__ == "__main__":
    main()