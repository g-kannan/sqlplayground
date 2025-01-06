import streamlit as st
import pandas as pd
import duckdb

token = st.secrets.backend.mdtoken
conn = duckdb.connect(f"md:interback?motherduck_token={token}") 

st.set_page_config(page_title="SQL Playground",layout="wide")
st.header("Welcome to SQLPlayground")
st.divider()

tab1, tab2, tab3 = st.tabs(["People", "customers", "organizations"])

with tab1:
    people_df = conn.sql("select * from people limit 50")
    st.dataframe(people_df,hide_index=True)
    st.divider()

with tab2:
    customers_df = conn.sql("select * from customers limit 50")
    st.dataframe(customers_df,hide_index=True)
    st.divider()

with tab3:
    organizations_df = conn.sql("select * from organizations limit 50")
    st.dataframe(organizations_df,hide_index=True)
    st.divider()

st.link_button("Click here for DuckDB documentation","https://duckdb.org/docs/sql/functions/overview")
st.divider()

st.write("SQL Query Editor")

query = st.text_input("Enter your SQL query", value="select * from people limit 10")
if st.button("Execute SQL"):
    result = conn.sql(query)
    st.dataframe(result,hide_index=True)

