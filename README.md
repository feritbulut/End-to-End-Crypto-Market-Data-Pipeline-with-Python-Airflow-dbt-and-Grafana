# End-to-End Crypto Market Data Pipeline

Bu proje, CoinGecko API kullanılarak kripto para piyasası verilerinin çekilmesi, işlenmesi ve analiz edilebilir hale getirilmesini kapsayan bir Data Engineering pipeline'ıdır.

## Mimari
- **Extract:** Python (Requests)
- **Raw Data Lake:** MinIO (S3 uyumlu)
- **Transform & Validate:** Pandas, PyArrow, Great Expectations
- **Data Warehouse:** PostgreSQL
- **Modeling:** dbt
- **Orchestration:** Apache Airflow
- **Containerization:** Docker

## Kurulum
(Docker Compose ve kurulum adımları ilerleyen aşamalarda eklenecektir.)