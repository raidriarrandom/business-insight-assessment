
import streamlit as st
import pandas as pd
from athena_helper import run_athena_query

st.title("Sales Trend")

st.header("Monthly Sales Over Time")
trend_df = run_athena_query("SELECT * FROM sales_trend ORDER BY order_month")
trend_df["total_sales"] = pd.to_numeric(trend_df["total_sales"])
st.line_chart(trend_df.set_index("order_month")["total_sales"])

st.header("Sales by Item Category")
category_df = run_athena_query("SELECT * FROM sales_by_category ORDER BY total_sales DESC")
category_df["total_sales"] = pd.to_numeric(category_df["total_sales"])
st.bar_chart(category_df.set_index("item_category")["total_sales"])
