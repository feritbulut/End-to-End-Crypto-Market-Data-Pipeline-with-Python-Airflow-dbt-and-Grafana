-- ==========================================
-- 2. WINDOW FUNCTIONS AND TIME SERIES ANALYSIS--
-- ==========================================

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