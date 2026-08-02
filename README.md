# 📊 End-to-End Crypto Market Data Pipeline

A production-ready, containerized data engineering pipeline that extracts real-time cryptocurrency market data from the CoinGecko API, processes and validates it, and loads it into a data warehouse for analytics and visualization.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Apache Airflow](https://img.shields.io/badge/Airflow-2.7.3-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

##  Overview

This project demonstrates a complete **ELT/ETL data pipeline** built with modern data engineering best practices. It ingests live cryptocurrency market data, applies data quality checks, and transforms raw data into analytics-ready tables for business intelligence.

### Key Features
-  **Real-time Data Extraction** from CoinGecko API with retry mechanisms
-  **Medallion Architecture** (Bronze → Silver → Gold layers)
-  **Data Quality Validation** using Great Expectations (Fail-Fast mechanism)
-  **Automated Orchestration** with Apache Airflow
-  **Data Modeling** with dbt (Data Build Tool)
-  **Interactive Dashboards** with Grafana
-  **Fully Containerized** with Docker & Docker Compose
-  **Clean Code** principles (SOLID, DRY, SRP)

---

##  Architecture

```
─────────────────┐
│  CoinGecko API  │
└────────────────┘
         │ HTTP GET (JSON)
         ▼
┌─────────────────┐
│  Python ETL     │
│  (Extract)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ─────────────────┐
│  MinIO (S3)     │     │  Great          │
│  Bronze Layer   │◄────┤  Expectations   │
│  (Raw JSON)     │     │  (Validation)   │
└────────┬────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐
│  Python ETL     │
│  (Transform)    │
└────────┬────────┘
         │ Parquet
         ▼
┌─────────────────┐
│  MinIO (S3)     │
│  Silver Layer   │
│  (Clean Parquet)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PostgreSQL     │
│  Data Warehouse │
────────┬────────┘
         │
         ▼
┌─────────────────┐
│  dbt            │
│  (Transform)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Analytics      │
│  (Gold Layer)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Grafana        │
│  (Dashboard)    │
└─────────────────┘
         ▲
         │
┌─────────────────┐
│  Apache Airflow │
│  (Orchestration)│
─────────────────┘
```

---

##  Technology Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Language** | Python 3.10 | Core ETL logic |
| **API** | CoinGecko REST API | Data source |
| **Data Lake** | MinIO (S3-compatible) | Raw & Silver storage |
| **Data Warehouse** | PostgreSQL 15 | Structured data storage |
| **Orchestration** | Apache Airflow 2.7.3 | Workflow scheduling |
| **Transformation** | dbt (Data Build Tool) | SQL-based modeling |
| **Data Quality** | Great Expectations | Validation & testing |
| **Visualization** | Grafana 10.2 | Dashboards & KPIs |
| **Containerization** | Docker & Docker Compose | Environment isolation |
| **Libraries** | Pandas, PyArrow, SQLAlchemy, Requests | Data processing |

---

##  Project Structure

```
crypto-market-pipeline/
│
├── airflow/                    # Airflow DAGs and plugins
│   └── dags/
│       └── crypto_pipeline_dag.py
│
├── dbt_crypto/                 # dbt project (data modeling)
│   ├── models/
│   │   ├── staging/
│   │   └── analytics/
│   └── dbt_project.yml
│
├── src/                        # Core Python ETL code
│   ├── extract/
│   │   └── coingecko.py
│   ├── transform/
│   │   └── cleaner.py
│   ├── load/
│   │   ├── minio_loader.py
│   │   ── postgres_loader.py
│   ├── validate/
│   │   └── data_validator.py
│   ├── utils/
│   │   ├── config.py
│   │   └── logger.py
│   └── main.py
│
── docker/                     # Docker configuration
│   ├── Dockerfile.etl
│   └── docker-compose.yml
│
├── queries/                    # SQL analysis queries
│   ├── 01_basic_analysis.sql
│   ├── 02_window_functions.sql
│   └── 03_cte_and_performance.sql
│
├── .env.example                # Environment variables template
├── .gitignore
├── requirements.txt
└── README.md
```

---

##  Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.10+ (optional, for local development)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/feritbulut/End-to-End-Crypto-Market-Data-Pipeline-with-Python-Airflow-dbt-and-Grafana.git
   cd crypto-market-pipeline
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services**
   ```bash
   cd docker
   docker compose up -d
   ```

4. **Run the ETL pipeline**
   ```bash
   docker compose up etl
   ```

5. **Run dbt transformations**
   ```bash
   cd ../dbt_crypto
   dbt run
   ```

### Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **Airflow** | http://localhost:8080 | admin / admin |
| **Grafana** | http://localhost:3000 | admin / admin123 |
| **MinIO Console** | http://localhost:9001 | minioadmin / minioadmin123 |
| **PostgreSQL** | localhost:5433 | crypto_user / crypto_password_123 |

---

##  Data Pipeline Flow

### 1. Extract
- Fetches top 50 cryptocurrencies by market cap from CoinGecko API
- Implements retry logic and rate limiting
- Saves raw JSON to MinIO (Bronze layer)

### 2. Transform
- Cleans data: removes duplicates, handles nulls, converts types
- Renames columns for schema consistency
- Converts to Parquet format (Silver layer)

### 3. Validate
- Applies Great Expectations rules:
  - `coin_id` must not be null
  - `current_price` must be > 0
  - `market_cap` must not be null
- **Fail-Fast**: Pipeline aborts if validation fails

### 4. Load
- Upserts coin metadata to `dim_coins` (Dimension table)
- Loads daily prices to `fact_daily_prices` (Fact table)
- Uses SQLAlchemy with connection pooling

### 5. Model (dbt)
- Creates staging views (`stg_coins`, `stg_daily_prices`)
- Builds analytics tables with window functions:
  - 7-day moving average
  - Market cap ranking
  - Daily volatility metrics

### 6. Visualize
- Grafana dashboards with:
  - KPI panels (top coin price)
  - Time series charts (price trends)
  - Dynamic filters (coin selection)

---

##  Key Concepts Demonstrated

### Data Engineering Principles
- **Medallion Architecture**: Bronze → Silver → Gold layers
- **Idempotency**: Safe retries without data duplication
- **Fail-Fast**: Immediate validation failures prevent bad data
- **Separation of Concerns**: Modular code structure (SRP)

### SQL & Analytics
- **Window Functions**: `ROW_NUMBER()`, `RANK()`, `LAG()`, `AVG() OVER()`
- **CTEs**: Readable complex queries
- **Star Schema**: Fact and Dimension tables
- **Performance**: Indexes and `EXPLAIN ANALYZE`

### Production Best Practices
- **Containerization**: Docker for environment consistency
- **Orchestration**: Airflow for scheduling and monitoring
- **Data Quality**: Great Expectations for validation
- **Version Control**: Git with conventional commits

---

##  Usage Examples

### Run ETL Pipeline Locally
```bash
python src/main.py
```

### Query Analytics Data
```sql
-- Top 10 coins by market cap with 7-day moving average
SELECT 
    coin_name,
    current_price,
    moving_avg_7d,
    market_cap_rank_daily
FROM analytics.fact_coin_daily_stats
ORDER BY market_cap_rank_daily
LIMIT 10;
```

### Trigger Airflow DAG
```bash
# Via CLI
airflow dags trigger crypto_market_pipeline

# Or use the web UI at http://localhost:8080
```

---

##  Sample Dashboard Metrics

- **Total Market Cap**: Sum of all coin market caps
- **Top Performer**: Coin with highest 24h price change
- **Volume Leaders**: Coins with highest trading volume
- **Price Trends**: Historical price movements with moving averages

---

##  Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

##  Author

**Ferit BULUT**  
Data Engineer | Building production-ready data pipelines

---

##  Acknowledgments

- [CoinGecko API](https://www.coingecko.com/api) for free cryptocurrency data
- [Apache Airflow](https://airflow.apache.org/) for workflow orchestration
- [dbt Labs](https://www.getdbt.com/) for data transformation framework
- [Great Expectations](https://greatexpectations.io/) for data validation

---

**⭐ If you find this project useful, please give it a star!**