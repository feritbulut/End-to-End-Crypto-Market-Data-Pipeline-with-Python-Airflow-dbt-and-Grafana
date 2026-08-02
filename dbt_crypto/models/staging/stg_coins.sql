{{ config(materialized='view') }}

SELECT 
    coin_id,
    UPPER(symbol) as symbol,
    INITCAP(name) as name,
    created_at,
    updated_at
FROM {{ source('crypto', 'dim_coins') }}