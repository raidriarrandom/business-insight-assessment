# Solution Design Document — Business Insight Assessment

> Status: Proposed architecture, built and reasoned through with AI assistance. Per the assessment's own requirements, this should still receive written SME approval (Ninad/Azmat/Kareem/Avirup) before being considered final — proceeding with implementation now given no response yet, per explicit instruction to move forward.

## Architecture

```
SQL Server RDS (BusinessAssessmentRDS)
        │  AWS DMS (full load)
        ▼
   S3 — raw/bronze layer (order_items, order_item_options, date_dim)
        │  AWS Glue (PySpark ETL job)
        ▼
   S3 — curated/gold layer (cleaned + joined + CLV & metrics computed)
        │  Glue Data Catalog
        ▼
   Athena (serverless SQL query layer)
        │
        ▼
   Streamlit dashboard (hosted on EC2, reads via Athena/boto3)
        │
   AWS Glue Workflow — daily batch schedule
```

## Rationale per component

- **AWS DMS** — purpose-built for extracting from a live database (SQL Server) into S3. Satisfies the requirement that ingestion originates from SQL Server, and that the pipeline uses AWS resources only (no Snowflake, no dbt).
- **AWS Glue (PySpark)** — the assessment explicitly mandates PySpark for transformations. Glue runs PySpark serverlessly (billed per DPU-hour when a job runs), avoiding the cost of an always-on EMR cluster. This is also where the known data integrity issues get handled:
  - Blank `USER_ID` rows (17,808 of them) — excluded from CLV calculation, flagged separately as anonymous/guest orders.
  - `date_dim` only covering 2023 while orders span 2020–2024 — extended/regenerated to cover the full order date range.
  - 28 orphaned `order_item_options` rows (referencing a non-existent `LINEITEM_ID`) — excluded from joins.
  - 156 rows with `ITEM_PRICE` ≤ 0 — retained but flagged, not silently dropped, per the assessment's instruction to report data issues rather than hide them.
- **S3 (raw + curated layers)** — standard separation between "what came from the source, untouched" and "what's ready for analysis," consistent with the medallion-style layering used in prior projects.
- **Athena** — serverless SQL over the curated S3 data. No separate always-on database needed for the query layer, keeping cost minimal.
- **Streamlit** — not explicitly named in this assessment's own doc, but consistent with the tool named in sibling academy assessments (Wistia, Calendly). Hosted on AWS (EC2) rather than external Streamlit Cloud, to stay within the "entire thing has to be done in AWS" constraint.
- **AWS Glue Workflow** — schedules the Glue ETL job to run once daily, matching the "processed daily once as a batch process" requirement.

## Primary metric: Customer Lifetime Value (CLV)

Calculated per customer (`USER_ID`) as total historical spend across all their orders (`ITEM_PRICE × ITEM_QUANTITY`, summed across `order_items`, plus any associated `order_item_options` charges), joined against `date_dim` for time-based segmentation. Rows with blank `USER_ID` are excluded from this calculation and reported separately as a data-quality caveat, not silently included or dropped without mention.

## Known limitations, reported per the assessment's own instruction to surface data issues

- `date_dim` required extension to cover the full 2020–2024 order date range.
- ~8.75% of `order_items` rows have no `USER_ID` and cannot be attributed to a customer's CLV.
- 28 rows in `order_item_options` reference a non-existent line item and are excluded from joins.
- Dashboard tool (Streamlit) is an inference from sibling project conventions, not explicitly named in this assessment's own requirements doc.
