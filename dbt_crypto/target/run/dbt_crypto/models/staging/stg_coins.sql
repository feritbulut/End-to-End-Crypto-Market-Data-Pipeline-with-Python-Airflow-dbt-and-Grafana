
  create view "crypto_dw"."analytics"."stg_coins__dbt_tmp"
    
    
  as (
    

SELECT 
    coin_id,
    UPPER(symbol) as symbol,
    INITCAP(name) as name,
    created_at,
    updated_at
FROM "crypto_dw"."public"."dim_coins"
  );