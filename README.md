# Unified People Data Platform

End-to-end system to:
- Ingest large people datasets (Apollo TSV, California CSV, Excel)
- Clean + deduplicate using PySpark
- Store unified data in PostgreSQL
- Expose a credit-based FastAPI for search & access

## Tech Stack

- **ETL**: PySpark, DuckDB, Pandas
- **Storage**: PostgreSQL
- **API**: FastAPI + Uvicorn
- **Auth & Credits**: API key, PostgreSQL tables (`users`, `api_keys`, `usage_logs`)

## Project Structure

```text
.
├─ pyspark_etl_unified.py           # Main ETL (Spark → Parquet)
├─ clean_california_duckdb.py       # DuckDB cleaner for California CSV
├─ load_parquet_to_postgres.py      # Load Parquet → PostgreSQL
├─ fastapi_unified_api/
│   ├─ main.py
│   ├─ db.py
│   ├─ auth.py
│   ├─ models.py         (optional)
│   ├─ routers/
│   │   ├─ search.py
│   │   ├─ credits.py
│   │   ├─ admin.py
│   │   └─ logs.py
│   └─ requirements.txt
└─ sample_data/ (optional small CSVs, not full 8GB)
