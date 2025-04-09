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

if 'cols_list' not in st.session_state:
    st.session_state.cols_list = '*'

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
dataset = st.selectbox("Select a dataset", ["people", "customers", "organizations","nyctaxi","custom"])
if dataset == "custom":
    place_holder_query = "SELECT * FROM <table_name> LIMIT 10"
elif dataset in ["nyctaxi"]:
    result_df = conn.sql(f"SELECT * FROM sample_data.nyc.taxi LIMIT 1").df()
    cols = result_df.columns
    cols_list = cols.tolist()
    st.session_state.cols_list = ', '.join(cols_list)
    place_holder_query = f"SELECT {st.session_state.cols_list} FROM sample_data.nyc.taxi limit 100;"
elif dataset in ["people", "customers", "organizations"]:
    result_df = conn.sql(f"SELECT * FROM {dataset} LIMIT 1").df()
    cols = result_df.columns
    cols_list = cols.tolist()
    st.session_state.cols_list = ', '.join(cols_list)
    place_holder_query = f"SELECT {st.session_state.cols_list} FROM {dataset} limit 100;"

query = st.text_area("Enter your SQL query", value=place_holder_query, height=200)
if st.button("Execute SQL"):
    try:
        result = conn.sql(query)
        st.dataframe(result, hide_index=True)
    except Exception as e:
        st.error(f"Error executing query: {e}")


st.divider()
st.link_button("Click here for DuckDB documentation","https://duckdb.org/docs/sql/functions/overview")