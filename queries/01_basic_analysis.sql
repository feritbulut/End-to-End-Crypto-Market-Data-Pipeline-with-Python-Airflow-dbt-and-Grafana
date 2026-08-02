-- ==========================================
-- 1. BASIC ANALYSIS QUESTIONS
-- ==========================================

-- 1.1. What are the total market capitalization and the average price?
SELECT 
    COUNT(*) AS total_coins,
    SUM(market_cap) AS total_market_cap,
    AVG(current_price) AS avg_price,
    MAX(current_price) AS max_price,
    MIN(current_price) AS min_price
FROM fact_daily_prices
WHERE price_date = CURRENT_DATE;

-- 1.2. Which are the top 5 coins by trading volume?
SELECT 
    c.name,
    c.symbol,
    f.total_volume,
    f.current_price
FROM fact_daily_prices f
JOIN dim_coins c ON f.coin_id = c.coin_id
WHERE f.price_date = CURRENT_DATE
ORDER BY f.total_volume DESC
LIMIT 5;

-- 1.3.Coins with the biggest gains and losses in the last 24 hours
SELECT 
    c.name,
    f.price_change_percentage_24h
FROM fact_daily_prices f
JOIN dim_coins c ON f.coin_id = c.coin_id
WHERE f.price_date = CURRENT_DATE
ORDER BY f.price_change_percentage_24h DESC
LIMIT 10;