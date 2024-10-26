from decimal import Decimal
from enum import StrEnum
from typing import Protocol

import pandas as pd
from pandantic import BaseModel


class TransactionTypes(StrEnum):
    INCOME = "Income"
    PURCHASE = "Purchase"


class TransactionSchema(BaseModel):
    """The expected schema of a transaction."""

    id: str
    created_date: str
    type: str
    description: str
    type: TransactionTypes
    category: str
    subcategory: str
    amount: Decimal
    account: str
    status: str


class BudgetData(Protocol):
    def get_transactions(self) -> pd.DataFrame:
        """Returns transaction data for the budget app"""
        ...

    def get_categories(self) -> list[str]:
        """Returns a list of the transaction categories"""
        ...

    def get_accounts(self) -> list[str]:
        """Returns a list of the accounts available in the data source"""
        ...

    def _validate_transactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate transactions"""
        ...
