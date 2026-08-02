from airflow import DAG
from airflow.operators.python import PythonOperator  # type: ignore
from datetime import datetime, timedelta
import sys
import os

PROJECT_ROOT = "/opt/airflow/project"
sys.path.append(PROJECT_ROOT)

from src.extract.coingecko import CoinGeckoExtractor
from src.transform.cleaner import DataCleaner
from src.load.minio_loader import MinIOLoader
from src.load.postgres_loader import PostgresLoader
from src.utils.config import AppConfig

default_args = {
    'owner': 'ferit',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}

def extract_data(**kwargs):
    config = AppConfig()
    extractor = CoinGeckoExtractor()
    coins = extractor.get_top_coins(limit=50)
    
    loader = MinIOLoader(
        endpoint=config.minio.endpoint,
        access_key=config.minio.access_key,
        secret_key=config.minio.secret_key,
        secure=False
    )
    loader.save_json_to_raw(bucket_name=config.minio.bucket_name, data=coins)
    print(f"Extracted and saved {len(coins)} coins.")

def transform_and_load_silver(**kwargs):
    config = AppConfig()
    
    extractor = CoinGeckoExtractor()
    coins = extractor.get_top_coins(limit=50)
    
    cleaner = DataCleaner()
    cleaned_df = cleaner.clean_coins_data(coins)
    
    loader = MinIOLoader(
        endpoint=config.minio.endpoint,
        access_key=config.minio.access_key,
        secret_key=config.minio.secret_key,
        secure=False
    )
    loader.save_parquet_to_silver(bucket_name=config.minio.bucket_name, df=cleaned_df)
    print("Transformed and saved to Silver layer.")

def load_to_warehouse(**kwargs):
    config = AppConfig()
    extractor = CoinGeckoExtractor()
    coins = extractor.get_top_coins(limit=50)
    
    cleaner = DataCleaner()
    cleaned_df = cleaner.clean_coins_data(coins)
    
    pg_loader = PostgresLoader(config.postgres)
    pg_loader.upsert_coins(coins)
    pg_loader.load_daily_prices(cleaned_df)
    print("Loaded to PostgreSQL Data Warehouse.")

# DAG 
with DAG(
    dag_id='crypto_market_pipeline',
    default_args=default_args,
    description='CoinGecko API\'den veri çekip Data Lake ve Warehouse\'a yükler.',
    schedule_interval='0 8 * * *', # Her gün saat 08:00'de çalış (UTC)
    start_date=datetime(2026, 1, 1),
    catchup=False, # Geçmişteki eksik çalışmaları telafi etme
    tags=['crypto', 'etl', 'portfolio']
) as dag:

    # Task'ları tanımla
    task_extract = PythonOperator(
        task_id='extract_raw_data',
        python_callable=extract_data,
    )

    task_transform = PythonOperator(
        task_id='transform_to_silver',
        python_callable=transform_and_load_silver,
    )

    task_load = PythonOperator(
        task_id='load_to_warehouse',
        python_callable=load_to_warehouse,
    )

    # Bağımlılıkları belirle (Dependency)
    # Önce extract, başarılı olursa transform, başarılı olursa load çalışacak.
    task_extract >> task_transform >> task_load