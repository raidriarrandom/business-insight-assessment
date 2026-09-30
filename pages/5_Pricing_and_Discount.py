import streamlit as st

st.title("Pricing & Discount Effectiveness")

st.warning("This metric cannot be calculated from the data provided. No discount, promotional-price, or original-vs-sale-price field exists anywhere in order_items or order_item_options — every column in both tables was checked. This is a structural data gap, documented as finding #7 in the data integrity findings, not a missed calculation.")

st.header("What Would Be Needed")
st.markdown("""
To calculate pricing and discount effectiveness, the source data would need at minimum:
- A discount amount or percentage applied per line item
- The original (pre-discount) price alongside the actual charged price
- A promo code or campaign identifier, to attribute discounts to specific pricing strategies

None of these exist in the current order_items or order_item_options tables.
""")
