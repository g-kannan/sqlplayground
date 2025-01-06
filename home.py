import streamlit as st
import pandas as pd
import duckdb
import hmac

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets.backend.password):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

token = st.secrets.backend.mdtoken
conn = duckdb.connect(f"md:interback?motherduck_token={token}") 

st.set_page_config(page_title="SQL Playground",layout="wide")
st.header("Welcome to SQLPlayground")
st.divider()

tab1, tab2, tab3,tab4 = st.tabs(["People", "customers", "organizations","nyctaxi"])

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

with tab4:
    nyctaxi_df = conn.sql("select * from sample_data.nyc.taxi limit 50")
    st.dataframe(nyctaxi_df,hide_index=True)
    st.divider()

st.write("SQL Query Editor")

query = st.text_input("Enter your SQL query", value="select * from people limit 10")
if st.button("Execute SQL"):
    result = conn.sql(query)
    st.dataframe(result,hide_index=True)


st.divider()
st.link_button("Click here for DuckDB documentation","https://duckdb.org/docs/sql/functions/overview")