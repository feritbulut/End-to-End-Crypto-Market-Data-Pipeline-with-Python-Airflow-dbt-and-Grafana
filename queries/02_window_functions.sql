-- ==========================================
-- 2. WINDOW FUNCTIONS AND TIME SERIES ANALYSIS--
-- ==========================================

-- Test data for window function checks
INSERT INTO fact_daily_prices (coin_id, price_date, current_price, market_cap, total_volume, high_24h, low_24h)
VALUES 
('bitcoin', '2026-07-25', 60000, 1200000000000, 20000000000, 61000, 59000),
('bitcoin', '2026-07-26', 61000, 1220000000000, 21000000000, 62000, 60000),
('bitcoin', '2026-07-27', 59000, 1180000000000, 19000000000, 61000, 58000),
('bitcoin', '2026-07-28', 62000, 1240000000000, 22000000000, 63000, 61000),
('bitcoin', '2026-07-29', 63000, 1260000000000, 23000000000, 64000, 62000),
('bitcoin', '2026-07-30', 64000, 1280000000000, 24000000000, 65000, 63000),
('bitcoin', '2026-07-31', 63500, 1270000000000, 23500000000, 64500, 62500),
('bitcoin', '2026-08-01', 63368, 1267000000000, 23368000000, 64000, 62000)
ON CONFLICT (coin_id, price_date) DO NOTHING;

-- 2.1. Market Capitalization Ranking (RANK) for Each Coin
SELECT 
    c.name,
    f.market_cap,
    RANK() OVER (ORDER BY f.market_cap DESC) AS market_cap_rank
FROM fact_daily_prices f
JOIN dim_coins c ON f.coin_id = c.coin_id
WHERE f.price_date = CURRENT_DATE;

-- 2.2. Bitcoin's Daily Price Change (LAG Function)
WITH btc_prices AS (
    SELECT 
        price_date,
        current_price
    FROM fact_daily_prices
    WHERE coin_id = 'bitcoin'
    ORDER BY price_date
)
SELECT 
    price_date,
    current_price,
    LAG(current_price, 1) OVER (ORDER BY price_date) AS previous_day_price,
    current_price - LAG(current_price, 1) OVER (ORDER BY price_date) AS daily_change
FROM btc_prices;

-- 2.3. 7-Day Moving Average
WITH btc_prices AS (
    SELECT 
        price_date,
        current_price
    FROM fact_daily_prices
    WHERE coin_id = 'bitcoin'
    ORDER BY price_date
)
SELECT 
    price_date,
    current_price,
    AVG(current_price) OVER (
        ORDER BY price_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_avg_7d
FROM btc_prices;