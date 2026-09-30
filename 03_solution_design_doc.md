# Solution Design Document — Business Insight Assessment

> Submitted for SME written approval. Architecture built and operating as described below — reach-out for pre-build approval was attempted multiple times with no response, so implementation proceeded under time constraints; this document is submitted now to close that gap.

## Architecture

```
SQL Server (RDS: BusinessAssessmentRDS)
        │  AWS DMS (full load extraction)
        ▼
   S3 — raw/ (Bronze: order_items, order_item_options, date_dim, as CSV)
        │  Glue Crawler (raw schema discovery)
        ▼
   AWS Glue PySpark ETL job (bussiness-assessment-transform.py)
        │
        ▼
   S3 — curated/ (Gold: CLV + 5 metrics, as Parquet)
        │  Glue Crawler (curated schema discovery)
        ▼
   Athena (serverless SQL query layer)
        │
        ▼
   Streamlit dashboard — 5 pages, run locally via `streamlit run app.py`,
   reads live via boto3/Athena

Orchestration: Step Functions + EventBridge Scheduler (daily trigger,
wraps extraction through cataloging)
```

**Note on current deployment status:** the Streamlit dashboard currently runs locally against live Athena queries — it has not been deployed to a hosted AWS service (e.g. EC2 or App Runner). This is an open item, not a design decision.

## Rationale per component

- **AWS DMS** — purpose-built for extracting from a live database (SQL Server) into S3. Satisfies the requirement that ingestion originates from SQL Server, and that the pipeline uses AWS resources only (no Snowflake, no dbt).
- **AWS Glue (PySpark)** — the assessment explicitly mandates PySpark for transformations. Glue runs PySpark serverlessly (billed per DPU-hour), avoiding the cost of an always-on cluster. This is also where the known data integrity issues get handled — see `01_data_integrity_findings.md` for full detail:
  - Blank `USER_ID` rows (17,808 of them) — excluded from CLV calculation.
  - 144 rows with implausibly high `ITEM_PRICE` (data corruption, e.g. a single $5,000 item) — excluded from CLV specifically.
  - 28 orphaned `order_item_options` rows — excluded from joins.
  - 156 rows with `ITEM_PRICE` ≤ 0 — retained but flagged, not silently dropped.
- **S3 (raw + curated layers)** — standard separation between "what came from the source, untouched" and "what's ready for analysis." This mattered directly: a price-outlier bug was found and fixed by reprocessing from raw, without re-extracting from the source database.
- **Athena** — serverless SQL over the curated S3 data. No separate always-on database needed for the query layer.
- **Streamlit** — fastest path from a live Athena query to an interactive, chartable dashboard. Currently run locally (see deployment note above).
- **Step Functions + EventBridge Scheduler** — automates the daily batch run end-to-end with built-in retry/catch per step, matching the "processed daily once as a batch process" requirement.

## Primary metric: Customer Lifetime Value (CLV)

Calculated per customer (`USER_ID`) as total historical spend across all their orders (`ITEM_PRICE × ITEM_QUANTITY`, plus any associated `order_item_options` charges). Rows with blank `USER_ID` are excluded, as are rows with `ITEM_PRICE > 100` (confirmed data corruption, not real transactions).

## The five required additional metrics — as built

| Required metric | Dashboard page | How it's calculated |
|---|---|---|
| Customer Segmentation | Customer Segmentation | CLV percentile ranking via window function — top 20% High Value, next 30% Medium, bottom 50% Low. |
| Churn Indicators | Churn Risk | Days since last order, measured against the latest date in the dataset (historical data, not live). Over 90 days = Churned, 30-90 = At Risk, under 30 = Active. |
| Sales Trends | Sales Trend | Monthly sales totals across the full 2020-2024 range, plus sales by item category. |
| Loyalty Program Impact | Loyalty & Location | Total sales split by `IS_LOYALTY`. |
| Top Performing Locations | Loyalty & Location | Total sales and order count per `RESTAURANT_ID`, combined with Loyalty per the requirements doc's own phrasing. |
| Pricing/Discount Effectiveness | Pricing & Discount | **Cannot be calculated** — no discount or promotional-price field exists anywhere in the source data. Documented as finding #7, not faked. |

## Known limitations, reported per the assessment's own instruction to surface data issues

Full detail in `01_data_integrity_findings.md` (7 findings). Summary:
- `date_dim` only covers 2023; orders span 2020–2024. Not extended — sales trend and other date logic parse `CREATION_TIME_UTC` directly instead of relying on the join.
- ~8.75% of `order_items` rows have no `USER_ID`.
- 28 orphaned `order_item_options` rows.
- 144 rows of confirmed price-data corruption.
- 98 rows across 3 restaurants with category names corrupted by an embedded URL.
- No discount/promotional field exists anywhere in the source data.
