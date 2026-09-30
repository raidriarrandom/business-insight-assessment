import streamlit as st
from athena_helper import run_athena_query

st.title("Churn Risk")

st.info("Churn status is measured against the most recent date present in the dataset (Feb 2024), not real time. Since this is historical data spanning 4 years, a high 'Churned' percentage is expected — it reflects how much of each customer's activity falls before the dataset's final snapshot date, not necessarily true customer attrition.")

st.header("Churn Status per Customer")
churn_df = run_athena_query("SELECT * FROM churn_indicator ORDER BY days_since_last_order DESC")
st.dataframe(churn_df)

st.header("Customers per Churn Status")
churn_counts_df = run_athena_query("SELECT churn_status, COUNT(*) AS customer_count FROM churn_indicator GROUP BY churn_status")
churn_counts_df["customer_count"] = churn_counts_df["customer_count"].astype(int)
st.bar_chart(churn_counts_df.set_index("churn_status")["customer_count"])
