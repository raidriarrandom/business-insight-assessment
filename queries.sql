-- Business Insight Assessment — Verification & Dashboard Queries
-- Run against Athena, database: business_assessment_db
-- These are the exact queries used to verify each metric's output and that power the Streamlit dashboard pages.

-- ============================================================
-- Customer Lifetime Value (primary metric) — app.py (home page)
-- ============================================================
SELECT * FROM customer_lifetime_value
ORDER BY customer_lifetime_value DESC
LIMIT 20;

-- Spot-check: verify a specific customer's order history behind their CLV number
-- (used to confirm the 1,801-order customer was a legitimate repeat customer, not corrupted data)
SELECT * FROM order_items_enriched
WHERE user_id = '5f1b00e5535ee93e0cb768e7'
ORDER BY creation_time_utc
LIMIT 20;


-- ============================================================
-- Customer Segmentation — pages/1_Customer_Segmentation.py
-- ============================================================
SELECT * FROM customer_segmentation
ORDER BY customer_lifetime_value DESC
LIMIT 20;

SELECT segment, COUNT(*) AS customer_count
FROM customer_segmentation
GROUP BY segment;


-- ============================================================
-- Churn Risk — pages/2_Churn_Risk.py
-- ============================================================
SELECT * FROM churn_indicator
ORDER BY days_since_last_order DESC;

SELECT churn_status, COUNT(*) AS customer_count
FROM churn_indicator
GROUP BY churn_status;


-- ============================================================
-- Sales Trend — pages/3_Sales_Trend.py
-- ============================================================
SELECT * FROM sales_trend
ORDER BY order_month;

-- Supplementary: sales by item category
SELECT * FROM sales_by_category
ORDER BY total_sales DESC;

-- Data quality spot-check: confirms the 98 rows with corrupted category names
-- (category value has an admin/menu-management URL spliced into it)
SELECT DISTINCT item_category, restaurant_id
FROM order_items_enriched
WHERE item_category LIKE '%http%';


-- ============================================================
-- Loyalty & Location Performance — pages/4_Loyalty_and_Location.py
-- ============================================================
SELECT * FROM sales_by_loyalty;

SELECT * FROM top_locations
ORDER BY total_sales DESC;


-- ============================================================
-- Pricing & Discount Effectiveness — pages/5_Pricing_and_Discount.py
-- ============================================================
-- No query — no discount/promotional-price field exists anywhere in the
-- source data (order_items or order_item_options). Verified by inspecting
-- every column in both raw tables. See finding #7 in 01_data_integrity_findings.md.


-- ============================================================
-- Raw data type/format diagnostics (used during debugging)
-- ============================================================
-- Confirmed creation_time_utc format (ISO 8601, e.g. 2023-02-16T06:33:33.041Z)
SELECT creation_time_utc FROM order_items_enriched LIMIT 5;

-- Confirmed date_dim's raw date_key column (col0) is stored as DD-MM-YYYY text,
-- not the ISO format used elsewhere — root cause of an earlier join bug
SELECT col0 FROM date_dim LIMIT 5;
