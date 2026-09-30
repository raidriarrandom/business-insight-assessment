import streamlit as st
from athena_helper import run_athena_query

st.title("Customer Segmentation")

st.header("Customer Segments by Lifetime Value")
segment_df = run_athena_query("SELECT * FROM customer_segmentation ORDER BY customer_lifetime_value DESC")
st.dataframe(segment_df)

st.header("Customers per Segment")
segment_counts_df = run_athena_query("SELECT segment, COUNT(*) AS customer_count FROM customer_segmentation GROUP BY segment")
segment_counts_df["customer_count"] = segment_counts_df["customer_count"].astype(int)
st.bar_chart(segment_counts_df.set_index("segment")["customer_count"])
