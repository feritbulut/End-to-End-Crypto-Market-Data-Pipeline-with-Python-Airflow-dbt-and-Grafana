-- ==========================================
-- 3. CTE AND PERFORMANCE ANALYSIS
-- ==========================================

-- 3.1. Readable Query with CTE: Find the Most Volatile Coins
WITH daily_stats AS (
    SELECT 
        coin_id,
        price_date,
        high_24h,
        low_24h,
        (high_24h - low_24h) / NULLIF(low_24h, 0) AS volatility
    FROM fact_daily_prices
    WHERE price_date = CURRENT_DATE
      AND low_24h > 0
)
SELECT 
    c.name,
    ds.volatility
FROM daily_stats ds
JOIN dim_coins c ON ds.coin_id = c.coin_id
ORDER BY ds.volatility DESC
LIMIT 10;

-- 3.2. Test Index Performance Using EXPLAIN ANALYZE

EXPLAIN ANALYZE
SELECT * 
FROM fact_daily_prices 
WHERE coin_id = 'bitcoin' 
  AND price_date = '2026-08-02';