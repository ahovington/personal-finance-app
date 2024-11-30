from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st
from config import BudgetData, TransactionTypes
from src_mockdata import BudgetDataMock


def budget_vs_actual(df: pd.DataFrame, categories: list[str]) -> dict[str:float]:
    # Budget vs Actual
    st.subheader("📊 Category Budgets")

    # Generate some sample budget limits
    budget_limits = {}
    for category in categories:
        actual_spending = df["spending_by_category"].get(category, 0)
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


def budget(budget_data: BudgetData) -> None:
    st.title("💰 Budget Planner: Budget")

    # refresh = st.sidebar.button("Refresh data")
    # if refresh:
    #     st.write("Refreshing the Datas...")
    #     budget_data.refresh_transactions()
    #     budget_data.refresh_accounts()
