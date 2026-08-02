import logging
import pandas as pd
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class DataCleaner:
    def __init__(self):
        logger.info("DataCleaner initialized")   

    def clean_coins_data(self, raw_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        CoinGecko ham verisini temizler.
        """
        df = pd.DataFrame(raw_data)
        logger.info(f"Raw data shape: {df.shape}")
        
        # 1. Gereksiz sütunları kaldır
        columns_to_keep = [
            'id', 'symbol', 'name', 'current_price', 'market_cap',
            'market_cap_rank', 'total_volume', 'high_24h', 'low_24h',
            'price_change_percentage_24h', 'last_updated'
        ]
        columns_to_keep = [col for col in columns_to_keep if col in df.columns]
        df = df[columns_to_keep]
        
        # 🌟 YENİ EKLEME: Veritabanı şemasıyla eşleşmesi için 'id' -> 'coin_id'
        if 'id' in df.columns:
            df = df.rename(columns={'id': 'coin_id'})
        
        # 2. Duplicate'leri kaldır (Artık 'coin_id' kullanıyoruz)
        initial_rows = len(df)
        df = df.drop_duplicates(subset=['coin_id'])
        duplicates_removed = initial_rows - len(df)
        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed} duplicate rows")
        
        # 3. Null değerleri kontrol et ve doldur
        null_counts = df.isnull().sum()
        if null_counts.sum() > 0:
            logger.warning(f"Null values found: {null_counts[null_counts > 0].to_dict()}")
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            df[numeric_cols] = df[numeric_cols].fillna(0)
        
        # 4. Veri tiplerini dönüştür
        df = self._convert_data_types(df)
        
        # 5. Tarih sütununu datetime'a çevir
        if 'last_updated' in df.columns:
            df['last_updated'] = pd.to_datetime(df['last_updated'])
        
        logger.info(f"Cleaned data shape: {df.shape}")
        logger.info(f"Columns: {list(df.columns)}") # Debug için sütunları logla
        
        return df
    
    def _convert_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
    
        numeric_columns = [
            'current_price', 'market_cap', 'total_volume',
            'high_24h', 'low_24h', 'price_change_percentage_24h'
        ]
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        if 'market_cap_rank' in df.columns:
            df['market_cap_rank'] = df['market_cap_rank'].astype('Int64') 
        
        return df