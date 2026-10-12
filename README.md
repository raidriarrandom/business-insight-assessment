# Business Insight Assessment — Customer Order Data Pipeline

An AWS-native, daily-batch pipeline that ingests order data from a SQL Server source, transforms it with PySpark, computes Customer Lifetime Value plus five additional business metrics, and serves the results through a live Streamlit dashboard.

## Business Objective

Turn raw order/transaction data into customer- and business-level insight: who the most valuable customers are (CLV and value segments), who is at risk of churning, how sales trend over time, what sells, whether loyalty status changes spending, and which locations perform best.

## Architecture

```
SQL Server (RDS)
  -> DMS (extract)
  -> S3 raw/ (Bronze, CSV)
  -> Glue Crawler (schema discovery)
  -> Glue PySpark job (bussiness-assessment-transform.py)
  -> S3 curated/ (Parquet: CLV + 5 metrics)
  -> Glue Crawler (curated schema)
  -> Athena (query layer)
  -> Streamlit dashboard (app.py)

Orchestration: Step Functions + EventBridge Scheduler (daily run)
```

Full design rationale: [`03_solution_design_doc.md`](03_solution_design_doc.md)

## Why Each Piece of the Stack

| Choice | Why |
|---|---|
| **AWS-only, no Snowflake/dbt** | Explicit hard requirement from the SME on the requirements call (see [`00_requirements_summary.md`](00_requirements_summary.md)) — not a preference, a constraint. |
| **DMS for extraction** | Purpose-built for continuous/one-time database migration out of RDS into S3, without hand-rolling a JDBC extraction script. |
| **Glue + PySpark for transformation** | Serverless Spark — no cluster to provision or manage, and the join/aggregation logic (order_items ⋈ order_item_options, CLV, the 5 metrics) genuinely needs a distributed dataframe engine, not just SQL over a warehouse. Also the only transformation engine allowed under the "no dbt" constraint. |
| **S3 medallion layout (raw/curated)** | Keeps the original extracted data immutable and replayable — if a transformation bug is found later (as happened with the price-outlier bug below), you reprocess from raw instead of re-extracting from the source database. |
| **Athena over a provisioned warehouse** | Serverless SQL directly against the curated Parquet files — no infrastructure to stand up just to query results. |
| **Streamlit for the dashboard** | Fastest path from a pandas DataFrame to an interactive, chartable UI, with a direct boto3/Athena connection under the hood (see `athena_helper.py`) rather than a heavier BI tool. |
| **Step Functions + EventBridge Scheduler** | Automates the daily run end-to-end (extract → transform → catalog) with built-in retry/catch per state, instead of a cron job with no failure visibility. |

## Data Model

Three source tables (`order_items`, `order_item_options`, `date_dim`) join into these curated Parquet tables:

- **`order_items_enriched`**: the full enriched fact table (item price × quantity + option totals = `LINE_TOTAL`)
- **`customer_lifetime_value`**: CLV, total line items, first/last order date, per `USER_ID`
- **`customer_segmentation`**: High / Medium / Low value, by CLV percentile (top 20% / next 30% / rest)
- **`churn_indicator`**: days since last order → Active (≤30), At Risk (31–90), Churned (>90)
- **`sales_trend`**: total sales per month
- **`sales_by_category`**: total sales per `ITEM_CATEGORY`
- **`sales_by_loyalty`**: total sales, loyalty vs. non-loyalty
- **`top_locations`**: total sales and distinct orders per `RESTAURANT_ID`

Full entity relationships, keys, and join logic: [`docs/er_diagram.png`](docs/er_diagram.png) ([editable source](docs/er_diagram.drawio))

## Known Data Quality Issues

Full writeup with row counts and root causes: [`01_data_integrity_findings.md`](01_data_integrity_findings.md). Highlights:

- 8.75% of `order_items` rows have a blank `USER_ID` (excluded from CLV)
- `date_dim` only covers 2023, while orders span 2020–2024, so date-dimension attributes (holiday, weekend) can't be applied to most orders
- 144 rows had implausible `ITEM_PRICE` values (e.g. $5,000 for a single item) — excluded from CLV via an `ITEM_PRICE <= 100` filter
- 98 rows across 3 restaurants have `ITEM_CATEGORY` values corrupted by an embedded admin/menu-management URL, spliced mid-string into the category name
- No discount or promo-price field exists in the source data, so Pricing & Discount Effectiveness can't be calculated; the dashboard page documents the gap instead

## Repository Structure

```
business-insight-assessment/
├── README.md
├── 00_requirements_summary.md
├── 01_data_integrity_findings.md        (7 documented data quality findings)
├── 02_rds_sqlserver_setup_summary.md
├── 03_solution_design_doc.md            (architecture rationale)
├── bussiness-assessment-transform.py    (Glue PySpark ETL: CLV + metrics)
├── athena_helper.py                     (boto3 Athena query helper)
├── app.py                               (Streamlit dashboard home page: CLV)
├── pages/                               (Streamlit pages, one per metric area)
│   ├── 1_Customer_Segmentation.py
│   ├── 2_Churn_Risk.py
│   ├── 3_Sales_Trend.py
│   ├── 4_Loyalty_and_Location.py
│   └── 5_Pricing_and_Discount.py
├── load_to_sql_server.py                (source data loader used during setup; reads RDS_PASSWORD env var)
├── queries.sql
├── table_cleanup.sql
├── docs/
│   ├── er_diagram.png
│   └── er_diagram.drawio
└── .github/workflows/ci.yml             (lint + syntax verification on push)
```

## Running the Dashboard Locally

```bash
pip3 install streamlit boto3 pandas
aws login --profile admin
cd business-insight-assessment
AWS_PROFILE=admin python3 -m streamlit run app.py
```

Requires AWS credentials with Athena/S3 read access to `business_assessment_db` and the `business-insight-assessment-499502048569` bucket.

## CI/CD

Every push to `main` triggers `.github/workflows/ci.yml`, which lints all Python files (flake8) and verifies syntax (`ast.parse`) on `app.py`, `athena_helper.py`, and the Glue transform script.

## SME Approval

Architecture and solution design were submitted for SME review per the project's approval requirement. Written approval is pending SME response as of submission.
