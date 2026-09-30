# Business Insight Assessment — Requirements Summary

> Condensed from the raw transcript (`00_requirements_call_transcript.md`). If anything here is ambiguous, check the raw transcript, not this summary.

Walkthrough of a business insight assessment: build a daily batch data engineering pipeline on AWS from SQL Server CSVs, using PySpark, to calculate customer lifetime value and related metrics, delivered via Streamlit dashboards with CI/CD.

## Assessment Setup & Source Data
- CSV order files provided via Google Drive; download and inspect for integrity or data issues and report findings.
- Analyze CSVs manually to design the schema/ER diagram; no automation allowed for this step.

## Pipeline Architecture & Tooling
- Source is SQL Server; entire pipeline must run on AWS resources only, no Snowflake, dbt, or other external tools.
- Detailed transformations must use PySpark; pipeline runs as a daily batch with scheduling included.
- Pipeline covers ingestion, transformation, business insight metrics, and dashboarding.
- Architecture diagram and solution design document require written SME approval before building; draw.io acceptable.

## Metrics & Dashboards
- Primary metric is Customer Lifetime Value; additional metrics defined with goal and calculation guidance.
- Additional insights: churn indicators, customer segmentation, sales trends, loyalty impact, top locations, pricing/discount effectiveness.
- Deliver separate Streamlit dashboards per metric area (segmentation, churn risk, sales trend, loyalty/location, pricing/discount).

## Deliverables & Submission
- Submit pipeline documentation, code files, Spark scripts, SQL queries, setup configs, and final dashboards.
- Implement a CI/CD pipeline for code and configuration, mirroring production-level deployment.
- Use clear naming conventions per document and present the work, including rationale for the chosen architecture.
- Doc includes hyperlinks: SSMS install and SQL loader videos for Windows, Azure Data Studio for macOS, plus a Streamlit dashboard walkthrough.

## Next Steps
- Download the order CSV files from the shared Google Drive link and inspect for data integrity issues.
- Manually design the schema/ER diagram from the CSVs.
- Draft the pipeline architecture diagram and solution design document, then obtain written SME approval before building.
- Build the AWS pipeline: ingestion from SQL Server, PySpark transformations, CLV and additional metric calculations, daily batch scheduling.
- Build Streamlit dashboards for segmentation, churn risk, sales trend, loyalty/location, and pricing/discount.
- Set up a CI/CD pipeline for the code and configurations.
- Submit all deliverables with clear naming conventions and present the work, explaining the architecture choice.

## Decisions Made
- Source database is SQL Server; pipeline must run entirely on AWS.
- PySpark is required for detailed transformations.
- Pipeline runs as a daily batch with scheduling.
- Dashboards must be built in Streamlit.
- Customer Lifetime Value is the primary metric.
- Snowflake, dbt, and other external tools are not permitted.
