from datetime import datetime, timedelta
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st

from common import get_filters
from config import BudgetData, TransactionTypes
from sources.mockdata import BudgetDataMock


def calculate_budget_metrics(df: pd.DataFrame) -> dict:
    """Calculate key budget metrics from transaction data"""
    total_income = df[df["type"] == TransactionTypes.INCOME]["amount"].sum()
    total_spending = df[df["type"] == TransactionTypes.PURCHASE]["amount"].sum()
    spending_by_category = (
        df[df["type"] == TransactionTypes.PURCHASE]
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )
    spending_by_subcategory = (
        df[df["type"] == TransactionTypes.PURCHASE]
        .groupby(["category", "subcategory"])["amount"]
        .sum()
        .sort_values(ascending=False)
    )
    spending_by_subcategory.index = spending_by_subcategory.index.map(
        "{0[0]}: {0[1]}".format
    )
    income_by_category = (
        df[df["type"] == TransactionTypes.INCOME]
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )
    income_by_subcategory = (
        df[df["type"] == TransactionTypes.INCOME]
        .groupby("subcategory")["amount"]
        .sum()
        .sort_values(ascending=False)
    )
    return {
        "total_income": total_income,
        "total_spending": total_spending,
        "spending_by_category": spending_by_category,
        "spending_by_subcategory": spending_by_subcategory,
        "income_by_category": income_by_category,
        "income_by_subcategory": income_by_subcategory,
    }


def create_category_card(category: str, spent: float, percent_of_total: float) -> None:
    color = "#ff4b4b"
    return f"""
    <div style="padding: 1rem; border-radius: 8px; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-weight: 600;">{category}</span>
            <span>${spent:,.2f} / {percent_of_total:,.2f}%</span>
        </div>
        <div style="background-color: #e0e0e0; border-radius: 4px; height: 8px;">
            <div style="width: {min(percent_of_total, 100)}%; background-color: {color}; height: 100%; border-radius: 4px;"></div>
        </div>
    </div>
    """


def hero_metrics(total_income: float, total_spending: float) -> None:
    """Display the hero metrics

    Args:
        total_income (float): The total income recieved for the period.
        total_spending (float): The total spending for the period.
    """
    # Display key metrics in a row
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${total_income:,.2f}")
    col2.metric("Total Spending", f"${total_spending:,.2f}")
    col3.metric("Profit/Loss", f"${(total_income - total_spending):,.2f}")

    # TODO: Break spending into discretionary and non discretionary


def trend_line_chart(df: pd.DataFrame, x: str, y: str, groupby: str) -> None:
    st.subheader("📈 Trend")
    fig = px.line(df, x=x, y=y, color=groupby, title=None)
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
    )
    st.plotly_chart(fig, use_container_width=True)


def transaction_listing(df: pd.DataFrame) -> None:
    st.subheader("📝 Largest Transactions")
    for _, tx in df.iterrows():
        st.markdown(
            f"""
            <div style="padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between;">
                    <span>{tx['description']}</span>
                    <span style="color: #ff4b4b;">${tx['amount']:,.2f}</span>
                </div>
                <div style="color: #666; font-size: 0.9rem;">
                    {tx['date'].strftime('%B %d, %Y')} • {tx['category']} • {tx['account']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def account_listing(df: pd.DataFrame) -> None:
    st.subheader("📝 Account Balances")
    st.markdown(
        f"""
            <div style="padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between;">
                    <span>Total Savings</span>
                    <span style="color: #2ca314">${df['balance'].sum():,.2f}</span>
                </div>
            </div>
            """,
        unsafe_allow_html=True,
    )
    for _, acc in df.iterrows():
        st.markdown(
            f"""
            <div style="padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between;">
                    <span>{acc['account_name']}</span>
                    <span style="color: #2ca314">${acc['balance']}</span>
                </div>
                <div style="color: #666; font-size: 0.9rem;">
                    {acc['account_type']} • {acc['ownership_type']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def category_breakdown(
    heading: str, spending_categories: dict[str, float], total_spending: float
) -> None:
    st.markdown(f"### {heading}")
    for category, spending in spending_categories.items():
        percent_of_total = (spending / total_spending) * 100
        st.markdown(
            create_category_card(category, spending, percent_of_total),
            unsafe_allow_html=True,
        )


def actuals_profit_loss(df: pd.DataFrame) -> None:
    # date to datetime
    # TODO: move to the budget_data class
    df["date"] = pd.to_datetime(df["created_date"], utc=True)

    # Calculate metrics
    metrics = calculate_budget_metrics(df)
    hero_metrics(metrics["total_income"], metrics["total_spending"])

    # Create two columns for the main content
    left_col, right_col = st.columns([2, 1])
    with left_col:
        # Chart trend
        trend_df = df.copy()
        trend_df["day"] = pd.to_datetime(trend_df["date"], utc=True).dt.date
        trend_df = (
            trend_df.groupby(["day", "type"]).agg({"amount": "sum"}).reset_index()
        )
        trend_dfs = []
        rolling_days = st.number_input("Trend Rolling Days", value=30)
        for transaction_type in TransactionTypes:
            # Add missing days
            _trend_df = (
                trend_df[trend_df["type"] == transaction_type][["day", "amount"]]
                .set_index("day")
                .asfreq("D")
            )
            # Calculate rolling sum
            _trend_df = (
                _trend_df.groupby(["day"])["amount"]
                .sum()
                .rolling(rolling_days)
                .sum()
                .reset_index()
            )
            _trend_df["type"] = transaction_type
            trend_dfs.append(_trend_df)

        trend_line_chart(pd.concat(trend_dfs), "day", "amount", "type")
        # Transaction list
        transaction_listing(
            df[df["type"] != TransactionTypes.INCOME]
            .sort_values("amount", ascending=False)
            .head(10)
        )
    with right_col:
        # Display category cards
        transaction_group = st.selectbox(
            "Pick transaction grouping", ["Category", "Subcategory"]
        )
        purchase_group_metrics = (
            metrics["spending_by_category"]
            if transaction_group == "Category"
            else metrics["spending_by_subcategory"]
        )
        income_group_metrics = (
            metrics["income_by_category"]
            if transaction_group == "Category"
            else metrics["income_by_subcategory"]
        )
        category_breakdown(
            "Income Breakdown",
            income_group_metrics,
            metrics["total_income"],
        )
        category_breakdown(
            "Purchase Breakdown",
            purchase_group_metrics,
            metrics["total_spending"],
        )


def actuals_balance_sheet(df: pd.DataFrame) -> None:
    with st.sidebar:
        account_listing(df)


def actuals(budget_data: BudgetData) -> None:
    st.title("💰 Budget Planner: Actuals")

    filters = get_filters(
        budget_data.get_accounts(),
        budget_data.get_categories(),
        budget_data.get_subcategories(),
    )
    # Get transaction data
    actuals_profit_loss(budget_data.get_transactions(**filters))
    actuals_balance_sheet(budget_data.get_account_balances())


if __name__ == "__main__":
    # Generate sample transactions
    generator = BudgetDataMock()
    actuals(generator)
