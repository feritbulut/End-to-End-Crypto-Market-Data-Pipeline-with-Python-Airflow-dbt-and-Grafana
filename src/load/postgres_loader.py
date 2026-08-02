import logging
from datetime import datetime, date
from typing import List, Dict, Any
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from src.utils.config import PostgresConfig

logger = logging.getLogger(__name__)


class PostgresLoader:
    
    def __init__(self, config: PostgresConfig):
        self.config = config
        self.engine = create_engine(
            config.connection_url,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True
        )
        logger.info("PostgreSQL engine initialized")
    
    def upsert_coins(self, coins_data: List[Dict[str, Any]]) -> int:

        query = text("""
            INSERT INTO dim_coins (coin_id, symbol, name, updated_at)
            VALUES (:coin_id, :symbol, :name, :updated_at)
            ON CONFLICT (coin_id) 
            DO UPDATE SET 
                symbol = EXCLUDED.symbol,
                name = EXCLUDED.name,
                updated_at = EXCLUDED.updated_at
        """)
        
        now = datetime.now()
        records = [
            {
                "coin_id": coin["id"],
                "symbol": coin["symbol"].upper(),
                "name": coin["name"],
                "updated_at": now
            }
            for coin in coins_data
        ]
        
        try:
            with self.engine.begin() as conn:
                result = conn.execute(query, records)
                row_count = result.rowcount
                logger.info(f"Upserted {row_count} coins to dim_coins")
                return row_count
        except SQLAlchemyError as e:
            logger.error(f"Failed to upsert coins: {e}")
            raise
    
    def load_daily_prices(self, df: pd.DataFrame) -> int:
        
        df_to_load = df.copy()
        df_to_load['price_date'] = df_to_load['last_updated'].dt.date if 'last_updated' in df_to_load.columns else date.today()
        
        columns_to_load = [
            'coin_id', 'price_date', 'current_price', 'market_cap',
            'market_cap_rank', 'total_volume', 'high_24h', 'low_24h',
            'price_change_percentage_24h', 'last_updated'
        ]
        
        available_columns = [col for col in columns_to_load if col in df_to_load.columns]
        df_to_load = df_to_load[available_columns]
        
        try:
            row_count = df_to_load.to_sql(
                name='fact_daily_prices',
                con=self.engine,
                if_exists='append',
                index=False,
                method='multi', 
                chunksize=1000   
            )
            logger.info(f"Loaded {row_count} rows to fact_daily_prices")
            return row_count
        except SQLAlchemyError as e:
            logger.error(f"Failed to load daily prices: {e}")
            raise
    
    def get_latest_price_date(self, coin_id: str = None) -> date:
        
        query = text("""
            SELECT MAX(price_date) as latest_date 
            FROM fact_daily_prices
            WHERE coin_id = :coin_id
        """) if coin_id else text("SELECT MAX(price_date) as latest_date FROM fact_daily_prices")
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(query, {"coin_id": coin_id} if coin_id else {})
                row = result.fetchone()
                return row[0] if row and row[0] else None
        except SQLAlchemyError as e:
            logger.error(f"Failed to get latest price date: {e}")
            raise