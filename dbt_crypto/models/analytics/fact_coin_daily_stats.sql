
{{ config(materialized='table') }}

WITH daily_prices AS (
    SELECT * FROM {{ ref('stg_daily_prices') }}
),
coins AS (
    SELECT * FROM {{ ref('stg_coins') }}
)

SELECT 
    dp.price_date,
    dp.coin_id,
    c.name as coin_name,
    c.symbol as coin_symbol,
    dp.current_price,
    dp.market_cap,
    dp.total_volume,
    dp.price_change_percentage_24h,
    AVG(dp.current_price) OVER (
        PARTITION BY dp.coin_id 
        ORDER BY dp.price_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7d,
    
    RANK() OVER (
        PARTITION BY dp.price_date 
        ORDER BY dp.market_cap DESC
    ) as market_cap_rank_daily
FROM daily_prices dp
JOIN coins c ON dp.coin_id = c.coin_id