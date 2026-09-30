import streamlit as st
from athena_helper import run_athena_query
import pandas as pd

st.title("Business Insight Assessment Dashboard")

st.header("Customer Lifetime Value")
clv_df = run_athena_query("SELECT * FROM customer_lifetime_value ORDER BY customer_lifetime_value DESC LIMIT 20")
st.dataframe(clv_df)


st.header("Sales by Item Category")
category_df = run_athena_query("SELECT * FROM sales_by_category ORDER BY total_sales DESC")
category_df["total_sales"] = pd.to_numeric(category_df["total_sales"])
st.bar_chart(category_df.set_index("item_category")["total_sales"])

st.header("Loyalty vs. Non-Loyalty Spend")
loyalty_df = run_athena_query("SELECT * FROM sales_by_loyalty")
loyalty_df["total_sales"] = pd.to_numeric(loyalty_df["total_sales"])
st.bar_chart(loyalty_df.set_index("is_loyalty")["total_sales"])

st.header("Holiday vs. Non-Holiday Sales")
holiday_df = run_athena_query("SELECT * FROM sales_by_holiday")
holiday_df["total_sales"] = pd.to_numeric(holiday_df["total_sales"])
st.bar_chart(holiday_df.set_index("is_holiday")["total_sales"])
