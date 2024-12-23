import random
from datetime import datetime, timedelta

import pandas as pd
from config import TransactionSchema, TransactionTypes
from faker import Faker


class BudgetDataMock:
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

    def get_transactions(
        self,
        start_date: datetime,
        end_date: datetime,
        account: str = None,
        excluded_categories: list[str] = None,
        excluded_subcategories: list[str] = None,
        validate_transactions: bool = True,
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
                    "account": random.choice(["Checking", "Credit Card"]),
                    "status": random.choice(["cleared", "pending"]),
                }
                transactions.append(transaction)

            current_date += timedelta(days=1)
        df = pd.DataFrame(transactions)
        if account:
            df = df[df["account"] == account]
        if excluded_categories:
            df = df[-df["category"].isin(excluded_categories)]
        if excluded_subcategories:
            _excluded_subcategories = [x.split(":")[1] for x in excluded_subcategories]
            df = df[-df["subcategory"].isin(_excluded_subcategories)]
        if validate_transactions:
            self._validate_transactions(df)
        return df

    def get_categories(self) -> list[str]:
        """Returns a idempptent list of categories"""
        return list(self.categories.keys())

    def get_subcategories(self) -> list[str]:
        """Returns a idempptent list of subcategories"""
        subcategories = []
        for value in self.categories.values():
            subcategories.append(value)
        return subcategories.sort()

    def get_accounts(self) -> list[str]:
        return ["Checking", "Credit Card"]

    def get_account_balances(self):
        return pd.DataFrame(
            {
                "account_name": ["Transaction", "Transaction", "Saver", "Saver"],
                "account_type": ["Transactional", "Transactional", "Saver", "Saver"],
                "ownership_type": ["Individual", "Joint", "Individual", "Joint"],
                "currency_code": ["AUD", "AUD", "AUD", "AUD"],
                "balance": [154, 300, 4500, 200],
            }
        )

    def refresh_transactions(self) -> None:
        """Refresh transactions data"""
        pass

    def refresh_accounts(self) -> None:
        """Refresh accounts data"""
        pass

    def _validate_transactions(self, df):
        # validate transactions
        TransactionSchema.parse_df(
            dataframe=df,
            errors="raise",
        )
