import streamlit as st
import pandas as pd
from athena_helper import run_athena_query

st.title("Loyalty & Location Performance")

st.header("Loyalty vs. Non-Loyalty Spend")
loyalty_df = run_athena_query("SELECT * FROM sales_by_loyalty")
loyalty_df["total_sales"] = pd.to_numeric(loyalty_df["total_sales"])
st.bar_chart(loyalty_df.set_index("is_loyalty")["total_sales"])

st.header("Top Performing Locations")
locations_df = run_athena_query("SELECT * FROM top_locations ORDER BY total_sales DESC")
locations_df["total_sales"] = pd.to_numeric(locations_df["total_sales"])
locations_df["total_orders"] = locations_df["total_orders"].astype(int)
st.dataframe(locations_df)

st.bar_chart(locations_df.set_index("restaurant_id")["total_sales"])
