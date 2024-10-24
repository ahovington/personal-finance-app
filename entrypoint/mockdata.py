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
                    "account": random.choice(["Checking", "Credit Card", "Cash"]),
                    "status": random.choice(["cleared", "pending"]),
                }
                transactions.append(transaction)

            current_date += timedelta(days=1)
        df = pd.DataFrame(transactions)
        if validate_transactions:
            self.validate_transactions(df)
        return df

    def validate_transactions(self, df):
        # validate transactions
        TransactionSchema.parse_df(
            dataframe=df,
            errors="raise",
        )
