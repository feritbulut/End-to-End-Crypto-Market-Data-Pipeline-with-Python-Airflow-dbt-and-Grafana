
CREATE TABLE IF NOT EXISTS dim_coins (
    coin_id VARCHAR(50) PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fact_daily_prices (
    id SERIAL PRIMARY KEY,
    coin_id VARCHAR(50) NOT NULL,
    price_date DATE NOT NULL,
    current_price DECIMAL(20, 8),
    market_cap DECIMAL(30, 2),
    market_cap_rank INTEGER,
    total_volume DECIMAL(30, 2),
    high_24h DECIMAL(20, 8),
    low_24h DECIMAL(20, 8),
    price_change_percentage_24h DECIMAL(10, 4),
    last_updated TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(coin_id, price_date)
);

CREATE INDEX IF NOT EXISTS idx_fact_prices_coin_id ON fact_daily_prices(coin_id);
CREATE INDEX IF NOT EXISTS idx_fact_prices_date ON fact_daily_prices(price_date DESC);
CREATE INDEX IF NOT EXISTS idx_fact_prices_coin_date ON fact_daily_prices(coin_id, price_date DESC);

COMMENT ON TABLE dim_coins IS 'Coin metadata - Dimension table';
COMMENT ON TABLE fact_daily_prices IS 'Daily price snapshots - Fact table';
COMMENT ON COLUMN fact_daily_prices.current_price IS 'USD cinsinden güncel fiyat';