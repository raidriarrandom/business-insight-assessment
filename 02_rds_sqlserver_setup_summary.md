# RDS SQL Server Setup — Summary

> Condensed from the raw transcript (`02_rds_sqlserver_setup_transcript.md`). If anything here is ambiguous, check the raw transcript, not this summary.

Video tutorial walking through creating a SQL Server RDS instance on AWS, connecting via SSMS, and loading CSV flat files into a new database for a data pipeline.

## Creating the RDS SQL Server Instance
- In the RDS console, use Standard Create and select Microsoft SQL Server Express Edition.
- Use Self-Managed credentials with a custom master password; leave engine defaults.
- Enable public access so a local machine can connect to upload raw data.
- Estimated cost around $34.27/month; keep minimum storage for non-enterprise use.

## Networking & Security Group
- Open the VPC security group tied to the new RDS instance from the instance details page.
- Edit inbound rules to allow all traffic from 0.0.0.0/0, delete the default rule, and save.
- Instance creation takes roughly 10 to 15 minutes; endpoint and port appear on the details page.

## SSMS Setup & Connection
- Download and install SSMS (SQL Server Management Studio) from the Microsoft page.
- Connect using SQL Server Authentication, pasting the RDS endpoint and master password.
- Check Trust Server Certificate with encryption optional, then Connect.

## Creating the Database & Loading Data
- Run a CREATE DATABASE query (e.g. Global Partners) via New Query, then refresh to view.
- Right-click the database, Tasks, Import Flat File to load provided CSV files.
- Schema defaults to `dbo`; preview data, allow nulls, then Finish to insert.
- Repeat the import for each flat file to populate all tables.
- Query the table (e.g. `global_partners.dbo.<table>`) to verify the loaded data.
