# Instacart Data Warehouse

An end-to-end data engineering project built with the Instacart Market Basket
Analysis dataset. The pipeline downloads the source data from Kaggle, loads
the CSV files into PostgreSQL, prepares a staging layer, and loads a
dimensional data warehouse orchestrated by Apache Airflow.

## Project Status

This project is complete as a portfolio and learning project. The pipeline
demonstrates the main workflow from raw data ingestion through dimensional
model loading, with Docker used to provide a reproducible runtime.

## Pipeline Overview

The Airflow DAG is named `instacart_data_warehouse` and follows this flow:

```text
extract_data
    ↓
ingest_to_postgres
    ↓
transform_data
    ↓
staging_to_dwh
```

### Processing steps

1. **Extract** - Download the
   `psparks/instacart-market-basket-analysis` dataset using KaggleHub and copy
   the CSV files into `data/raw`.
2. **Ingest** - Create the raw tables and copy the CSV contents into the
   PostgreSQL `raw` schema.
3. **Transform** - Combine and cast source columns into the `staging`
   tables:
   `staging.products`, `staging.orders`, and `staging.order_products`.
4. **Load** - Truncate and reload the dimensional warehouse tables, then add
   and validate foreign-key constraints.

## Architecture

![ETL Pipeline](./assets/ELT%20Pipeline.png)

### Data layers

- `raw` - landing layer containing the source CSV tables
- `staging` - cleaned and typed tables used by the warehouse load
- `dw` - dimensional model for analytics

### Data warehouse model

The warehouse uses a simple star schema:

- `dw.dim_product` - product, aisle, and department attributes
- `dw.dim_order` - order and customer activity attributes
- `dw.fact_order_items` - order-product facts, including cart position and
  reorder status

![Star Schema](./assets/medium/Star_Schema.png)

## Tech Stack

| Technology | Purpose |
| --- | --- |
| Python | ETL logic |
| Apache Airflow 3 | Orchestration |
| PostgreSQL 16 | Raw, staging, and warehouse storage |
| Pandas | CSV processing |
| SQLAlchemy | Database interaction |
| KaggleHub | Dataset download |
| Docker Compose | Containerized Airflow runtime |

## Project Structure

```text
.
├── assets/
│   ├── ETL Pipeline.png
│   └── medium/
├── dags/
│   └── instacart_dag.py
├── data/
│   └── raw/
├── docker/
│   └── docker-compose.yaml
├── scripts/
│   ├── connection.py
│   ├── extract.py
│   ├── load_raw.py
│   ├── profiling.py
│   ├── staging_to_dwh.py
│   └── transform.py
├── sql/
│   ├── 01_create_schema.sql
│   └── 02_create_table_dw.sql
└── README.md
```

## Getting Started

### Prerequisites

- Docker Desktop with Docker Compose
- A PostgreSQL database accessible from the Airflow containers
- Kaggle credentials configured for KaggleHub

### Configuration

Create a `.env` file in the project root. This file is intentionally excluded
from version control.

```env
DB_HOST=<postgres-host>
DB_NAME=<database-name>
DB_USER=<database-user>
DB_PASSWORD=<database-password>
DB_PORT=<postgres-port>
```

The database connection used by the DAG must be registered in Airflow with the
connection ID `instacart_postgre`.

### Run the services

The Compose configuration expects an external Docker network named
`docker_pgnetwork`:

```bash
docker network create docker_pgnetwork
docker compose -f docker/docker-compose.yaml up -d
```

Open the Airflow UI at <http://localhost:8080> and log in with the credentials
configured through `_AIRFLOW_WWW_USER_USERNAME` and
`_AIRFLOW_WWW_USER_PASSWORD` in `.env` (or the Compose defaults).

Before the first DAG run, apply the SQL files in `sql/` to the target
PostgreSQL database to create the `raw`, `staging`, and `dw` schemas and the
warehouse tables. Then enable and trigger the `instacart_data_warehouse` DAG
from the Airflow UI.

## Expected Output

A successful run completes the tasks in order and leaves the following
warehouse tables ready for analytics:

```text
dw.dim_product
dw.dim_order
dw.fact_order_items
```

Because the Instacart dataset is static, the DAG is intended to be triggered
manually when needed rather than continuously processing new source data.

## Related Article

The process and design decisions are also documented in the Medium article:

[From Raw CSV to Data Warehouse: Building an End-to-End Data Engineering
Pipeline with PostgreSQL, Docker, and Apache
Airflow](https://medium.com/@HafizIkhsan/from-raw-to-data-warehouse-building-an-end-to-end-data-engineering-pipeline-with-postgresql-c1bea0e206dd)

## Disclaimer

This project was built as part of a learning journey in data engineering. It
is a portfolio implementation and may be extended with production concerns
such as stronger data-quality checks, secrets management, incremental loading,
and automated tests.
