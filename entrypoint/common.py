import datetime as dt
from typing import Any
import streamlit as st


def get_filters(
    accounts: list[str], categories: list[str], subcategories: list[str]
) -> dict[str:Any]:
    ## Config for sidebar
    # Date range selection
    st.sidebar.header("Budget Filters")
    end_date = dt.datetime.now()
    start_date = end_date - dt.timedelta(days=365)
    try:
        start_date, end_date = st.sidebar.date_input(
            "Select Date Range", value=(start_date, end_date)
        )
    except ValueError:
        st.warning("Select start and end date from the date range in the sidebar.")

    # Other transaction filters
    account = st.sidebar.selectbox("Account", accounts, None)
    excluded_categories = st.sidebar.multiselect("Exclude categories", categories)
    excluded_subcategories = st.sidebar.multiselect(
        "Exclude subcategories", subcategories
    )
    return {
        "start_date": start_date,
        "end_date": end_date,
        "account": account,
        "excluded_categories": excluded_categories,
        "excluded_subcategories": excluded_subcategories,
    }
