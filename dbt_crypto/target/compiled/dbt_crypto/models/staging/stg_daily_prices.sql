

SELECT 
    id,
    coin_id,
    price_date,
    current_price,
    market_cap,
    market_cap_rank,
    total_volume,
    high_24h,
    low_24h,
    price_change_percentage_24h,
    last_updated,
    created_at
FROM "crypto_dw"."public"."fact_daily_prices"
WHERE current_price > 0