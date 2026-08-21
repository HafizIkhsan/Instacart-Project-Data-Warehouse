# Instacart Project Data Warehouse

An end-to-end ETL pipeline built using the Instacart Market Basket Analysis dataset. The pipeline automatically downloads data from Kaggle, ingests it into PostgreSQL, transforms it through a staging layer, and loads it into a dimensional data warehouse. Apache Airflow is used to orchestrate and schedule the entire workflow.

## Overview

The pipeline consists of the following steps:

1. Dataset download from Kaggle (`psparks/instacart-market-basket-analysis`)
2. Raw ingestion from CSV to PostgreSQL schema `raw`
3. Data transformation into schema `staging`
4. Data warehouse loading into schema `dw`
5. Automated scheduling and dependency handling with Airflow

## Architecture

### Airflow Task Flow

`download_data() >> ingest() >> transform_data() >> load_data()`

![ETL Pipeline](./assets/ETL%20Pipeline.png)

### Data Layers

- 📥 `raw`: landing layer for source CSV tables
- 🧩 `staging`: cleaned and prepared intermediate layer
- 🏛️ `dw`: dimensional model for analytics

Core warehouse tables:

- `dw.dim_product`
- `dw.dim_order`
- `dw.fact_order_items`

## Tech Stack

| Technology     | Purpose                             |
| -------------- | ----------------------------------- |
| Python         | ETL logic                           |
| Apache Airflow | Orchestration and scheduling        |
| PostgreSQL     | Raw, staging, and warehouse storage |
| Pandas         | Data processing                     |
| SQLAlchemy     | Database interaction                |
| KaggleHub      | Dataset download                    |
| Docker         | Containerized runtime               |

## Scheduling

- ⏰ Cron: `0 2 * * *` (daily at 02:00 WIB)
- ✅ `catchup=False` to avoid backfilling historical runs

Note: Since the Instacart dataset is static, the daily schedule is primarily used to demonstrate automated pipeline execution with Airflow.

## Project Structure

```text
.
├── assets/
├── dags/
│   └── instacart_dag.py
├── data/
│   └── raw/
├── scripts/
│   ├── connection.py
│   ├── ingestion.py
│   ├── load.py
│   ├── pipeline.py
│   ├── profiling.py
│   └── transform.py
└── README.md
```

## Getting Started

### Prerequisites

- Docker
- Kaggle account + API credentials

### Setup

1. Clone repository.
2. Provide environment variables in `.env`.
3. Configure Kaggle credentials for the Airflow runtime.
4. Start your environment (for example with Docker Compose, if used in your local setup).
5. In Airflow, create PostgreSQL connection ID: `instacart_postgres`.
6. Trigger DAG: `instacart_data_warehouse`.

## Expected Output

A successful run should complete all tasks in order:

`download_data -> ingest -> transform_data -> load_data`

After that, dimensional tables in schema `dw` are ready for analytics.

## Disclaimer ⚠️

This project was built as part of my learning journey in Data Engineering. It is continuously being improved as I explore new tools, best practices, and more advanced data engineering concepts.
