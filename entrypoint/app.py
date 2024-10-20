# app.py
import json
import random
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st
from faker import Faker
from config import TransactionSchema, TransactionTypes


st.set_page_config(
    page_title="Budget Application",
    page_icon="💵",
    layout="wide",
    initial_sidebar_state="auto",
)

# Date range selection
st.sidebar.header("Date Range")
end_date = datetime.now()
start_date = end_date - timedelta(days=365)
start_date, end_date = st.sidebar.date_input(
    "Select Date Range", value=(start_date, end_date)
)


class TransactionGenerator:
    def __init__(self):
        self.fake = Faker()
        self.categories = {
            "Income": ["Wages", "Dividends", "Rent"],
            "Housing": ["Rent", "Mortgage", "Insurance", "Maintenance"],
            "Transportation": ["Gas", "Car Payment", "Public Transit", "Repairs"],
            "Food": ["Groceries", "Restaurants", "Coffee Shops"],
            "Utilities": ["Electricity", "Water", "Internet", "Phone"],
            "Healthcare": ["Insurance", "Medications", "Doctor Visits"],
            "Entertainment": ["Movies", "Streaming Services", "Hobbies"],
            "Shopping": ["Clothing", "Electronics", "Home Goods"],
            "Other": ["Gifts", "Miscellaneous"],
        }
        self.category_ranges = {
            "Income": (500, 4000),
            "Housing": (800, 2000),
            "Transportation": (50, 500),
            "Food": (30, 200),
            "Utilities": (50, 300),
            "Healthcare": (20, 400),
            "Entertainment": (10, 100),
            "Shopping": (20, 300),
            "Other": (10, 200),
        }

    def generate_transactions(
        self, start_date: datetime, end_date: datetime
    ) -> pd.DataFrame:
        transactions = []
        current_date = start_date

        while current_date <= end_date:
            # Generate 2-5 transactions per day
            daily_transactions = random.randint(2, 5)

            for _ in range(daily_transactions):
                category = random.choice(list(self.categories.keys()))
                subcategory = random.choice(self.categories[category])
                amount_range = self.category_ranges[category]

                transaction = {
                    "id": self.fake.uuid4(),
                    "created_date": current_date.strftime("%Y-%m-%d"),
                    "description": f"{self.fake.company()} - {subcategory}",
                    "type": (
                        TransactionTypes.INCOME
                        if category == "Income"
                        else TransactionTypes.PURCHASE
                    ),
                    "category": category,
                    "subcategory": subcategory,
                    "amount": round(random.uniform(*amount_range), 2),
                    "account": random.choice(["Checking", "Credit Card", "Cash"]),
                    "status": random.choice(["cleared", "pending"]),
                }
                transactions.append(transaction)

            current_date += timedelta(days=1)

        return pd.DataFrame(transactions)


class BudgetPlanner:
    def __init__(self, categories):
        self.categories = categories

    def calculate_budget_metrics(self, df: pd.DataFrame) -> dict:
        """Calculate key budget metrics from transaction data"""
        total_income = df[df["category"] == TransactionTypes.INCOME]["amount"].sum()
        total_spending = df[df["category"] != TransactionTypes.INCOME]["amount"].sum()
        spending_by_category = df.groupby("category")["amount"].sum()
        daily_spending = df.groupby("created_date")["amount"].sum()

        return {
            "total_income": total_income,
            "total_spending": total_spending,
            "spending_by_category": spending_by_category,
            "daily_average": total_spending / len(df["created_date"].unique()),
            "daily_spending": daily_spending,
        }

    def generate_spending_forecast(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate spending forecast based on historical data"""
        monthly_spending = (
            df.groupby(
                [
                    pd.to_datetime(df["created_date"]).dt.year,
                    pd.to_datetime(df["created_date"]).dt.month,
                    "category",
                ]
            )["amount"]
            .sum()
            .reset_index()
        )

        avg_spending = monthly_spending.groupby("category")["amount"].mean()
        forecast = pd.DataFrame(
            {"category": avg_spending.index, "projected_amount": avg_spending.values}
        )

        return forecast


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
    col3.metric("Profit/Loass", f"${(total_income - total_spending):,.2f}")

    # TODO: Break spending into discretionary and non discretionary


def trend_line_chart(df: pd.DataFrame) -> None:
    st.subheader("📈 Trend")
    fig = px.line(df, x="date", y="amount", color="type", title=None)
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
        <div style="background-color: black; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
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


def budget_progress(metrics: pd.DataFrame, categories: list[str]) -> None:
    st.markdown("### Purchase Breakdown")
    for category in categories:
        if category == TransactionTypes.INCOME:
            continue
        spent = metrics["spending_by_category"].get(category, 0)
        percent_of_total = (spent / metrics["total_spending"]) * 100
        st.markdown(
            create_category_card(category, spent, percent_of_total),
            unsafe_allow_html=True,
        )


def budget_app(df: pd.DataFrame, planner: BudgetPlanner) -> None:
    st.title("💰 Budget Planner: Actuals")

    # Convert to DataFrame
    df["date"] = pd.to_datetime(df["created_date"])

    # Calculate metrics
    metrics = planner.calculate_budget_metrics(df)
    hero_metrics(metrics["total_income"], metrics["total_spending"])

    # Create two columns for the main content
    left_col, right_col = st.columns([2, 1])
    with left_col:
        # Chart trend
        trend_df = df[
            df["type"].isin([TransactionTypes.INCOME, TransactionTypes.PURCHASE])
        ]
        trend_df = (
            trend_df.groupby(["date", "type"])["amount"]
            .sum()
            .rolling(30)
            .sum()
            .reset_index()
        )
        trend_line_chart(trend_df)
        # Transaction list
        transactions_df = df.sort_values("amount", ascending=False).head(10)
        transaction_listing(transactions_df)
    with right_col:
        # Display category cards
        budget_progress(metrics, planner.categories)


if __name__ == "__main__":
    # Generate sample transactions
    generator = TransactionGenerator()
    transactions = generator.generate_transactions(start_date, end_date)

    # validate transactions
    df_raised_error = TransactionSchema.parse_df(
        dataframe=pd.DataFrame(transactions),
        errors="filter",
    )
    # Initialize budget planner
    # TODO: Remove budget planner as a class,
    # pass the category list as an input to the budget app
    planner = BudgetPlanner(list(generator.categories.keys()))
    budget_app(transactions, planner)


# TODO: Save for the budget page
# def budget_vs_actual(df: pd.DataFrame, categories: list[str]) -> dict[str:float]:
#     # Budget vs Actual
#     st.subheader("📊 Category Budgets")

#     # Generate some sample budget limits
#     budget_limits = {}
#     for category in categories:
#         actual_spending = df["spending_by_category"].get(category, 0)
#         suggested_budget = actual_spending * 1.1  # 10% buffer
#         budget_limits[category] = st.slider(
#             f"{category}",
#             0.0,
#             suggested_budget * 2,
#             suggested_budget,
#             step=50.0,
#             key=f"budget_{category}",
#         )
#     return budget_limits
