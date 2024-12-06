from datetime import datetime, timedelta
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st
from config import BudgetData, TransactionTypes
from src_mockdata import BudgetDataMock


def get_mean_spending_by_category(
    df: pd.DataFrame,
    date_part: str = "M",
    transaction_ts_name: str = "created_date",
    category_name: str = "category",
    transaction_amount_name: str = "amount",
) -> dict[str:float]:
    _df = df.copy()
    _df["date_part"] = pd.to_datetime(_df[transaction_ts_name], utc=True).dt.to_period(
        date_part
    )
    # Sum expenses by date part
    _df = (
        _df[["date_part", category_name, transaction_amount_name]]
        .groupby(["date_part", category_name])
        .agg({transaction_amount_name: "sum"})
    ).reset_index()
    # Average expenses over all date parts
    _df = (
        _df[[category_name, transaction_amount_name]]
        .groupby([category_name])
        .agg({transaction_amount_name: "mean"})
    )
    return _df.to_dict()["amount"]


def budget_vs_actual(category_spending: dict[str:float]) -> dict[str:float]:
    # Budget vs Actual
    st.subheader("📊 Category Budgets")

    # Generate some sample budget limits
    budget_limits = {}
    for category, actual_spending in category_spending.items():
        suggested_budget = actual_spending * 1.1  # 10% buffer
        budget_limits[category] = st.slider(
            f"{category}",
            0.0,
            suggested_budget * 2,
            suggested_budget,
            step=50.0,
            key=f"budget_{category}",
        )
    return budget_limits


def get_filters(
    accounts: list[str], categories: list[str], subcategories: list[str]
) -> dict[str:Any]:
    ## Config for sidebar
    # Date range selection
    st.sidebar.header("Budget Filters")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
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


def budget(budget_data: BudgetData) -> None:
    st.title("💰 Budget Planner: Budget")

    # refresh = st.sidebar.button("Refresh data")
    # if refresh:
    #     st.write("Refreshing the Datas...")
    #     budget_data.refresh_transactions()
    #     budget_data.refresh_accounts()

    filters = get_filters(
        budget_data.get_accounts(),
        budget_data.get_categories(),
        budget_data.get_subcategories(),
    )
    left_col, right_col = st.columns([2, 1])
    budget_date_part = left_col.selectbox("Pick budget period", ["Month", "Week"])
    transaction_group = right_col.selectbox(
        "Pick transaction grouping", ["category", "subcategory"]
    )
    date_part_map = {"Month": "M", "Week": "W"}
    set_budget = budget_vs_actual(
        get_mean_spending_by_category(
            df=budget_data.get_transactions(**filters),
            date_part=date_part_map[budget_date_part],
            category_name=transaction_group,
        )
    )
    st.write(set_budget)
