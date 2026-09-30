# Data Integrity Findings — Business Insight Assessment Source Files

> Findings from manual inspection of the three provided source files, per Step 1 of the assessment ("if you look at the actual files, you will be able to see if there are any problems with the files... you need to find and report it"). Verified with a real CSV parser (Python `csv` module) — an initial naive line-based pass (`awk`/`wc -l`) produced several false positives due to a quoted field containing an embedded newline; those are noted below and corrected.

## Files and real row counts
- `date_dim.csv`: 365 rows
- `order_items.csv`: 203,519 rows
- `order_item_options.csv`: 193,017 rows

## Confirmed issues

1. **17,808 rows (~8.75%) in `order_items` have a blank `USER_ID`.** Significant, since Customer Lifetime Value is the primary metric — an order with no customer ID can't be attributed to any customer's CLV. Needs a decision: exclude these from CLV calculation, or treat as anonymous/guest checkout and handle separately.

2. **`date_dim` only covers the year 2023** (all 365 rows are year=2023), but `order_items.CREATION_TIME_UTC` actually spans **2020-04-21 through 2024-02-21** — five calendar years. A large portion of order data has no matching `date_dim` row to join against for any date-attribute analysis (day-of-week, holiday flag, weekend flag). This is a structural gap in the provided dimension, not a fixable data-quality issue in the fact data — needs to be reported as a limitation, and likely requires extending the date dimension to cover the full order date range.

3. **28 rows in `order_item_options` reference a `LINEITEM_ID` that does not exist in `order_items`.** Orphaned foreign keys — these option rows can never be joined to a real order line item and would need to be excluded or flagged during ingestion.

4. **156 rows in `order_items` have `ITEM_PRICE` ≤ 0.** Could be legitimate free/promotional items or bad data — needs a judgment call, but is being reported rather than silently dropped.

5. **144 rows have implausibly high `ITEM_PRICE` values (> $100), most paired with unusually round, large `ITEM_QUANTITY` values (e.g., 500, 300, 213).** Examples: "Korean Kimchi" at $5,000 × 500 units = $2.5M for a single line item; "Espresso - Double" at $1,125 × 500 units = $562,500. Real price distribution: median $8, 99.9th percentile $78 — these 144 rows are clear outliers, not real transactions. Left unfiltered, they would completely corrupt the CLV metric (a handful of users would show millions of dollars in "lifetime value" from a single anomalous row). **Decision: excluded from the CLV calculation specifically** (kept in the raw/enriched dataset, not deleted from the source) using a threshold of `ITEM_PRICE <= 100`. Discovered during Glue transformation while sanity-checking CLV output — not caught in the original manual file inspection, since that pass only checked for prices ≤ 0, not implausibly high ones.

## Minor issues
- 1 row in `order_items` has a blank `LINEITEM_ID`.
- 1 row in `order_items` has `ITEM_QUANTITY` ≤ 0.
- No issues found with `CURRENCY` (all populated, all `USD`), `IS_LOYALTY` (all populated, `TRUE`/`FALSE` only), or negative `OPTION_PRICE` in `order_item_options` (none found).

## Note on tooling accuracy
An initial pass using `awk -F','` and `wc -l` reported several issues that turned out to be false positives — e.g. a false "3,900 rows with bad price," a false "12 malformed timestamps." Root cause: at least one row contains a quoted CSV field with a literal embedded newline (`"MANDARIN CARDAMOM\nJUICE"` as an `ITEM_NAME`), which is valid CSV per spec but breaks naive line-based parsing by splitting one logical row into two physical lines. All numbers above are from a proper CSV-aware parse (Python's `csv` module) and have been verified against the raw file content directly.

## 98 rows across 3 restaurants have `ITEM_CATEGORY` values corrupted by an embedded admin/menu-management URL.** Affected categories: `BBQ
  Plates` (restaurant `622289bc6863d23d066d56ff`), `Drip Coffee` (restaurant `62f2ce9824813746ce6f5140`), and `Kid's` (restaurant
  `6054db3295b70198148b456d`). This isn't a simple appended suffix — in the `Drip Coffee` case, the URL is spliced directly into the middle of the
  word (`Drip C` + URL + `offee`), confirming the corruption is a mid-string insertion, not concatenation at the end. Each affected restaurant's own
  admin URL appears embedded in its own corrupted rows, suggesting a per-restaurant export bug in whatever menu system generated this data, rather
  than random noise. **Decision:** left as-is in the raw/enriched dataset (not deleted from source, consistent with how other findings are handled),
  but noted here since it produces 3 ugly category labels in the `sales_by_category` metric rather than the clean `BBQ Plates`, `Drip Coffee`, and
  `Kid's` values. [Your call: decide whether to clean these 3 specific values before the `sales_by_category` aggregation, or leave them as documented
  known issues — state whichever you choose.]

