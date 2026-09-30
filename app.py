import streamlit as st
from athena_helper import run_athena_query

st.title("Business Insight Assessment Dashboard")

st.header("Customer Lifetime Value")
clv_df = run_athena_query("SELECT * FROM customer_lifetime_value ORDER BY customer_lifetime_value DESC LIMIT 20")
st.dataframe(clv_df)
