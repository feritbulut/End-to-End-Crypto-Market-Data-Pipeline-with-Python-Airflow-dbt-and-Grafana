

SELECT 
    coin_id,
    UPPER(symbol) as symbol,
    INITCAP(name) as name,
    created_at,
    updated_at
FROM "crypto_dw"."public"."dim_coins"